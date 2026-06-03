# Day 23 — Retry Logic, DLQ & Reliability Engineering 😄🔥

## Main Focus

Today’s focus was:

* retry mechanisms
* DLQ (Dead Letter Queue)
* failure handling
* Kafka message lifecycle
* reliability engineering concepts

This was less about APIs and more about:
“How distributed systems behave during failures?”

---

# Topics Covered

## Retry Logic Reintegration

Reintroduced retry flow into Kafka consumer.

Flow implemented:

* Consumer processes event
* Failure occurs
* retry_count increments
* Event republished into signup-events
* After retry limit → move to DLQ

---

# DLQ (Dead Letter Queue)

Created:

* signup-events-dlq topic

Learned:

* purpose of DLQ
* handling permanently failed events
* isolating bad messages from healthy pipeline

Successfully verified:

* failed messages entering DLQ topic

---

# Kafka Console Consumer

Learned difference between:

## kafka-topics

Used for:

* create topic
* delete topic
* describe topic

## kafka-console-consumer

Used for:

* reading messages from topics

Command used:

```bash id="2cyr2z"
bin/windows/kafka-console-consumer.bat --topic signup-events-dlq --from-beginning --bootstrap-server localhost:9092
```

---

# Kafka Retention Behavior

Observed that:
retry messages still remained in signup-events topic.

Learned:
Kafka topics are append-only logs.

Messages remain until:

* retention expiry
* cleanup policy

Important realization:
Kafka is NOT a traditional queue that immediately deletes processed messages.

---

# Edge Case Identified

Discovered logic issue:

retry_count = 3 was still re-entering signup-events before going to DLQ.

Original logic:

```python id="mn4q5h"
if retry_count < 3
```

Corrected to:

```python id="97ydpm"
if retry_count < 2
```

This ensured:
retry_count = 3 directly enters DLQ instead of re-entering main topic.

Important learning:
Distributed systems require careful edge-case thinking.

---

# Reliability Engineering Concepts

Understood:
Distributed systems are designed around failure handling.

Discussed:

* transient failures
* retries
* consumer crashes
* duplicate processing
* idempotency
* DLQ strategies

---

# Artificial Failure Simulation

Implemented:
random transient failures using:

```python id="6v4fph"
random.randint(1,5)
```

instead of static:

```python id="vgc8o0"
if username == "fail"
```

Learned:
Controlled artificial failures are common during local backend testing.

---

# Windows + Kafka Issue

Encountered:

```text id="kcjlwm"
AccessDeniedException
```

Learned:

* Windows file locking issues
* Kafka log/checkpoint behavior
* temporary metadata reset after deleting kraft-combined-logs

---

# Current Backend Architecture

Client
↓
FastAPI Signup Route
↓
Kafka Producer
↓
signup-events Topic
↓
Kafka Consumer
↓
Retry Logic
↓
DLQ Handling
↓
Service Layer
↓
PostgreSQL

---

# Biggest Learning Today

Backend systems are not just about:
“making things work”

They are about:
“making systems survive failures safely”.

This is the beginning of reliability engineering mindset.
