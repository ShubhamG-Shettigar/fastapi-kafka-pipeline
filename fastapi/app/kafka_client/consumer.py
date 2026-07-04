from kafka import KafkaConsumer, KafkaProducer
import json, sqlite3, logging, time, psycopg2, random
from app.kafka_client.producer import producer, publish_events
from app.db.postgres import *
from app.services.auth_service import create_user, hash_password
from app.models.schemas import UserSignup
from app.metrics import (processed_events_total, retry_events_total, dlq_events_total, consumer_lag)
from prometheus_client import start_http_server

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
processed_count = 0
retry_events = 0
dlq_events = 0

start_http_server(8001)
logging.info("Prometheus metrics server started on port 8001")

for message in consumer:
    consumer_lag.set(0)
    try:
        data = message.value
        print(data, flush=True)
        cursor = get_cursor()
        user = UserSignup(**data)
        #Implementing transient errors for DLQ logic
        if random.randint(1,20) == 2:
            raise Exception("Temporary DB failure")
        create_user(user, cursor)
        conn.commit()
        logging.info("User inserted successfully")
        consumer.commit()
        logging.info(f"Offset committed= {message.offset}")
       # processed_count += 1
       #Replacing with counters
        processed_events_total.inc()

    except Exception as e:
        conn.rollbacdlwk()
        retry_count = data.get("retry_count", 0)
        if retry_count<1:
            data["retry_count"] = retry_count + 1
            logging.warning(f"Retrying event... Attempt = {data['retry_count']}")
            logging.info("\n")
            publish_events("signup-events", data)
            #retry_events += 1
            #Replacing with counters
            retry_events_total.inc()
        else:
            logging.error("Retry limit exhausted.. Moving the event to DLQ")
            publish_events("signup-events-dlq", data)
            #dlq_events += 1
            #Replacing with counters
            dlq_events_total.inc()
        consumer.commit()
        logging.error(f"Processing failed: {e}")
    #logging.info(f"Stats => processed = {processed_count}, retries = {retry_events}, dlq = {dlq_events}")
    logging.info(f"Stats => processed = {processed_events_total}, retries = {retry_events_total}, dlq = {dlq_events_total}")