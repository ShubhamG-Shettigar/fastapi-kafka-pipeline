import json
import logging
from kafka import KafkaConsumer
from app.configs.settings import settings
from app.db.postgres import get_connection
from app.kafka_client.retry_handler import handle_failure


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

consumer = KafkaConsumer(
    settings.kafka_order_status_topic, settings.kafka_order_status_retry_topic,
    bootstrap_servers=settings.kafka_bootstrap_servers,
    auto_offset_reset="earliest",
    enable_auto_commit=False,
    group_id="order_status_group",
    value_deserializer=lambda message: json.loads(
        message.decode("utf-8")
    )
)
logging.info("Order status consumer started")
for message in consumer:
    data = message.value
    logging.info(f"Received status event: {data}")
    try:
        connection = get_connection()
        cursor = connection.cursor()
        try:
            order_id = data["payload"]["order_id"]
            cursor.execute(
            """
            UPDATE orders_wrong
            SET status = 'CONFIRMED'
            WHERE order_id = %s
            """,
            (order_id,))
            connection.commit()
        finally:
            cursor.close()
            connection.close()
        consumer.commit()
        logging.info(f"Order {order_id} marked as CONFIRMED")
        logging.info(f"Offset committed = {message.offset}")
    except Exception as e:
        logging.error(f"Status event processing failed: {e}")
        result = handle_failure(data, settings.kafka_order_status_retry_topic, settings.kafka_order_status_dlq_topic)
        consumer.commit()
        logging.info(f"Event handling result = {result}")