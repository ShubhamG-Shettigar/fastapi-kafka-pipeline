from kafka import KafkaConsumer, KafkaProducer
import json, sqlite3, logging, time, psycopg2, random
from kafka_client.producer import producer, publish_events
from db.postgres import *
from services.auth_service import create_user, hash_password
from models.schemas import UserSignup

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("Consumer started")

producer = KafkaProducer(
    bootstrap_servers = "localhost:9092",
    value_serializer = lambda v: json.dumps(v).encode("utf-8")

)
consumer = KafkaConsumer(
    "signup-events",
    bootstrap_servers="localhost:9092",
    auto_offset_reset='earliest',
    enable_auto_commit=False,
    group_id='orders_group',
    value_deserializer=lambda m: json.loads(m.decode("utf-8"))
)

consumer.poll(timeout_ms = 1000)
logging.info(f"Assigned partitions: {consumer.assignment()}")
time.sleep(5)
#logging.info("Connecting to DB")
for message in consumer:
    try:
        data = message.value
        print(data, flush=True)
        cursor = get_cursor()
        user = UserSignup(**data)
        #Implementing transient errors for DLQ logic
        if random.randint(1,3) == 3:
            raise Exception("Temporary DB failure")
        create_user(user, cursor)
        conn.commit()
        consumer.commit()
        print("User inserted successfully", flush=True)

    except Exception as e:
        conn.rollback()
        retry_count = data.get("retry_count", 0)
        if retry_count<2:
            data["retry_count"] = retry_count + 1
            publish_events("signup-events", data)
        else:
            publish_events("signup-events-dlq", data)
        consumer.commit()
        print(f"Error: {e}", flush=True)