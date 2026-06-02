# Day 22 — Interview Concepts & Kafka Reliability 😄🔥

## Topics Covered

### Kafka Consumer Failure Scenario

Scenario discussed:

* Consumer processes message
* DB insert succeeds
* Before `consumer.commit()`
* Consumer crashes

---

# Problem Identified

When consumer restarts:

Kafka re-delivers same message because:

* offset was not committed

This can lead to:

* duplicate DB inserts
* duplicate processing

---

# Core Concept Learned

## Idempotency 😄🔥

Meaning:
Processing same event multiple times should not corrupt system state.

---

# Solutions Discussed

### DB-level uniqueness

Using:

* unique constraints
* primary keys
* message_id tracking

to safely reject duplicate events.

---

# Important Interview Concepts

## Kafka Offset Commit

Learned:

* Kafka does NOT know DB transaction state
* Kafka only tracks committed offsets

Therefore:

* DB commit and Kafka offset commit are separate operations

---

# Important Backend Thinking

Understood why:

* consumer crashes can cause duplicates
* distributed systems need defensive design
* exactly-once processing is difficult

---

# Interview-Level Answer Prepared

“If consumer crashes after DB commit but before Kafka offset commit, Kafka re-delivers the same message after restart.

This can cause duplicate processing.

To avoid this, we implement idempotency using:

* unique constraints
* message IDs
* deduplication logic.”

---

# Overall Progress

Current backend architecture now includes:

* FastAPI
* Kafka Producer
* Kafka Consumer
* PostgreSQL
* Service Layer
* Event-driven processing

Strong transition happening from:
“API developer”
to:
“distributed backend engineer”.
