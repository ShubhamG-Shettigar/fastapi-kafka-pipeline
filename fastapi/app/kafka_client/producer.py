import json
from kafka import KafkaProducer
from app.configs.settings import settings

producer = KafkaProducer(
    bootstrap_servers=settings.kafka_bootstrap_servers,
    value_serializer=lambda value: json.dumps(value).encode("utf-8")
)

def publish_event(data, topic = None):
    topic = topic or settings.kafka_orders_topic
    print(f"Publishing Kafka event to {topic}...")
    producer.send(topic,value=data)