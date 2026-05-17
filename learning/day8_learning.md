# Day 8 - Retry Mechanism + DLQ Architecture

## Topics Covered

* Kafka Retry Mechanism
* Dead Letter Queue (DLQ)
* Consumer-as-Producer Pattern
* Replay-safe retries
* Retry event republishing
* Failure observability
* DLQ PostgreSQL persistence
* Retry storms and cascading failures
* Distributed systems bottleneck reasoning

---

# Retry Architecture

Current flow:

FastAPI
↓
Kafka Topic (orders)
↓
Consumer Group
↓
PostgreSQL

If processing fails:

Consumer
↓
Retry Logic
↓
Re-publish event to Kafka
↓
OR move to DLQ

---

# Important Understanding

Kafka retries are NOT:

* same message replay forever

Instead:

* consumer republishes NEW retry events

Original failed offset is committed after handling.

---

# Retry Flow

1. Message consumed
2. Processing failure occurs
3. retry_count checked
4. If retries remain:

   * increment retry_count
   * republish event
5. Else:

   * move event to DLQ
6. Commit original failed offset

---

# DLQ Understanding

DLQ does NOT mean:

* data loss

DLQ means:

* message requires manual/special handling

Benefits:

* prevents infinite retries
* isolates poison messages
* avoids pipeline blockage
* improves observability

---

# producer.flush()

producer.send() buffers internally.

producer.flush() forces:

* immediate network send
* broker acknowledgement wait

Used to reduce risk of losing retry events before commit.

---

# Important Distributed Systems Concepts

## Retry Storm

Retries themselves create additional load.

High retries + slow DB:

* increases Kafka traffic
* increases DB pressure
* increases CPU usage
* increases lag

System starts overloading itself.

---

# Bottleneck Identification

Increasing Kafka partitions alone does NOT solve DB bottlenecks.

If DB is slow:

* more consumers can worsen pressure

Need:

* backoff
* batching
* indexing
* retry control

---

# PostgreSQL DLQ Table

Created:

CREATE TABLE dlq_users (
id SERIAL PRIMARY KEY,
message_id UUID,
name VARCHAR(100),
surname VARCHAR(100),
failed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

---

# Commands Used

## List Topics

bin/kafka-topics.sh --bootstrap-server localhost:9092 --list

## Create DLQ Topic

bin/kafka-topics.sh 
--bootstrap-server localhost:9092 
--create 
--topic orders_dlq 
--partitions 1 
--replication-factor 1

---

# Key Learning

Reliable distributed systems are NOT systems where failures never happen.

They are systems where failures are safely handled.
