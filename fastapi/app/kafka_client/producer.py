from kafka import KafkaProducer
#from app.kafka.producer import producer
import json, uuid

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def publish_events(topic, data):
    print("Publishing kafka event................")
    producer.send(topic, value=data)
    producer.flush()