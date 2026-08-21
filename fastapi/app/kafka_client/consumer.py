import json, logging
from kafka import KafkaConsumer
from app.configs.settings import settings
from app.kafka_client.retry_handler import handle_failure
from app.metrics import processed_events_total
from app.db.postgres import get_connection

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
consumer = KafkaConsumer(
    settings.kafka_orders_topic,
    settings.kafka_retry_topic,
    bootstrap_servers=settings.kafka_bootstrap_servers,
    auto_offset_reset="earliest",
    enable_auto_commit=False,
    group_id="orders_group",
    value_deserializer=lambda message: json.loads(
        message.decode("utf-8")
    )
)
logging.info("Kafka consumer started")
for message in consumer:
    data = message.value
    try:
        logging.info(f"Received event: {data}")
        connection = get_connection()
        cursor = connection.cursor()
        try:
            payload = data["payload"]
            cursor.execute(
                """
                INSERT INTO orders (event_id, order_id, customer_name, amount)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (event_id) DO NOTHING
                """,
                (
                    data["event_id"],
                    payload["order_id"],
                    payload["customer_name"],
                    payload["amount"]
                )
            )
            connection.commit()
        finally:
            cursor.close()
            connection.close()
        processed_events_total.inc()
        consumer.commit()
        logging.info(f"Offset committed = {message.offset}")

    except Exception as e:
        logging.error(f"Event processing failed: {e}")
        result = handle_failure(data)
        consumer.commit()
        logging.info(f"Event handling result = {result}")