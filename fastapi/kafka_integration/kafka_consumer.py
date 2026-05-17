from kafka import KafkaConsumer, KafkaProducer
import json, sqlite3, logging, time, psycopg2

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
    "orders",
    bootstrap_servers="localhost:9092",
    auto_offset_reset='latest',
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
        
        logging.info(f"Received message from partition: {message.partition}, offset {message.offset}")
        #conn = sqlite3.connect("users.db")
        #cursor = conn.cursor()
        
        
        conn = psycopg2.connect(host="localhost", database="kafka_project",
        user="postgres", password="postgresql", port="5432")
        
        cursor = conn.cursor()
        
        #logging.info("Connected to DB successfully")
        #logging.info("Cautious!!!! DB insert ongoing")
        #cursor.execute("Insert into shubham (name, surname, message_id) VALUES (?,?,?)",(data["name"], data["surname"], data["message_id"]))
        #logging.info("Hurray!!!! DB insert done")
        
        
        if data["name"] == "fail":
            raise Exception("Simulated processing failure")
        cursor.execute("Insert into users (message_id, name, surname) Values (%s, %s, %s)", (data["message_id"], data["name"], data["surname"]))
        logging.info("Cautious!!!! DB commit ongoing")
        conn.commit()
        logging.info("Hurray!!!! DB commit done")
        time.sleep(10)
        
        
        consumer.commit()
        logging.info(f"Consumer has committed offset = {message.offset}")
        logging.info("Hurray!!!! consumer commit done")
    
    except sqlite3.IntegrityError:
        logging.info("Duplicate message ignored safely")
        consumer.commit()
        logging.warning("A duplicate message was now committed")

    except Exception as e:
        logging.error(f"Real processing failure: {e}")
        retry_count = data.get("retry_count",0)
        logging.warning(f"Need to retry: {retry_count}")
        time.sleep(5)
        if retry_count < 3:
            data["retry_count"] = retry_count + 1
            producer.send("orders", value = data)
            producer.flush()
            logging.warning(f"Retrying message. Attempt {data['retry_count']}")
           
        else:
            producer.send("orders_dlq", value=data)
            producer.flush()
            logging.error("Message moved to DLQ")
            cursor.execute("Insert into dlq_users (message_id, name, surname) Values (%s, %s, %s)", (data["message_id"], data["name"], data["surname"]))
            conn.commit()
            logging.info("Committed into DLQ DB table")
        consumer.commit()
        time.sleep(5)
        logging.info(f"Consumer has committed offset = {message.offset}")
        
        