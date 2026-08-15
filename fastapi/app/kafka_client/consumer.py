import json, logging
from kafka import KafkaConsumer
from app.configs.settings import settings
from app.services.retryhandler import handle_failure
from app.metrics import processed_events_total


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
consumer = KafkaConsumer(
    settings.kafka_orders_topic,
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
        # Event processing will be added here
        # PostgreSQL/business processing will come later
        processed_events_total.inc()
        consumer.commit()
        logging.info(f"Offset committed = {message.offset}")
    except Exception as e:
        logging.error(f"Event processing failed: {e}")
        result = handle_failure(data)
        consumer.commit()
        logging.info(f"Event handling result = {result}")