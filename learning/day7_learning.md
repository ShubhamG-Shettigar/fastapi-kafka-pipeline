# Day 7 Learning 🚀

## Topics Covered

* Kafka partitions
* Consumer groups
* Multi-consumer scaling
* Rebalancing
* Sticky partition assignment
* PostgreSQL integration with Kafka consumer

---

# PostgreSQL Integration

Migrated Kafka consumer from:

* SQLite
  to:
* PostgreSQL using psycopg2

---

## PostgreSQL Connection

Used:

```python
psycopg2.connect(
    host="localhost",
    database="kafka_project",
    user="postgres",
    password="***",
    port="5432"
)
```

---

## PostgreSQL Insert Query

Learned PostgreSQL placeholders:

```python
%s
```

instead of SQLite placeholders:

```python
?
```

---

## Idempotency Validation

Tested crash scenario:

Flow:

* DB insert successful
* Consumer crashed before Kafka commit
* Consumer restarted
* Same message replayed by Kafka
* PostgreSQL UNIQUE(UUID) constraint prevented duplicate insert
* Consumer safely committed offset afterward

Validated:

* replay-safe consumer behavior
* idempotent event processing

---

# Kafka Partitions

Created new Kafka topic:

```bash
bin/kafka-topics.sh \
--bootstrap-server localhost:9092 \
--create \
--topic orders \
--partitions 3 \
--replication-factor 1
```

Verified using:

```bash
bin/kafka-topics.sh \
--bootstrap-server localhost:9092 \
--describe \
--topic orders
```

Observed:

* 3 partitions created successfully

---

# Sticky Partitioning

Produced multiple events without partition key.

Observed Kafka producer behavior:

* messages temporarily stick to same partition
* batching optimization occurs
* partitions later switch automatically

Example observed:

* first few messages → partition 0
* next few → partition 2
* later → partition 1

Learned:

* Kafka uses sticky partitioning for throughput optimization

---

# Multi-Consumer Experiment

Ran:

* 3 consumer instances
* same consumer group

Observed:

* each consumer received one partition
* parallel consumption achieved

Validated:

* maximum parallelism depends on partition count

---

# Extra Consumer Experiment

Started 4th consumer instance.

Observed:

* extra consumer remained idle
* assigned partition set was empty

Reason:

* only 3 partitions available

Learned:

* maximum active consumers per group = number of partitions

---

# Rebalancing Experiment

Tested:

* consumer joins
* consumer shutdown
* idle consumer leaving
* consumer restart

Observed:

* rebalance triggered on joins/leaves
* heartbeat/session timeout controls failure detection
* sticky assignment minimizes partition movement

Also observed:

* partition ownership may still change during rebalance
* sticky assignment is best-effort, not guaranteed ownership preservation

---

# Important Kafka Learnings

## Kafka Ordering Guarantee

Ordering exists:

* within a partition

NOT:

* across entire topic

---

## Offset Commit Behavior

Kafka commits:

* latest offset position

NOT:

* individual message acknowledgements

Higher offset commit implicitly marks earlier offsets as processed.

---

# Key Distributed Systems Learnings

Today introduced:

* real consumer-group coordination
* partition ownership
* dynamic rebalancing
* distributed parallel consumption
* fault-tolerant scaling concepts

Project is now transitioning toward:

* scalable distributed backend architecture
