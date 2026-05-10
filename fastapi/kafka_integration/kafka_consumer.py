from kafka import KafkaConsumer
import json, sqlite3, logging, time

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("Consumer started")

consumer = KafkaConsumer(
    "shubham",
    bootstrap_servers="localhost:9092",
    auto_offset_reset='latest',
    enable_auto_commit=False,
    group_id='shubham_group',
    value_deserializer=lambda m: json.loads(m.decode("utf-8"))
)


logging.info("Connecting to DB")
for message in consumer:
    try:
        data = message.value
        logging.info(f"Received message: {data}")
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        logging.info("Connected to DB successfully")
        logging.info("Cautious!!!! DB insert ongoing")
        cursor.execute("Insert into shubham (name, surname) VALUES (?,?)",
                   (data["name"], data["surname"]))
        logging.info("Hurray!!!! DB insert done")
       
        #logging.info("Cautious!!!! DB commit ongoing")
        conn.commit()
        time.sleep(10)
        consumer.commit()
        logging.info(f"Consumer has committed offset = {message.offset}")
        #logging.info("Hurray!!!! DB commit done")
    except Exception as e:
        logging.error(f"Some error occurred:{e}")
    
