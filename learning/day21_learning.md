# Day 21 — Event Driven Signup Architecture 😄🔥

## Major Architectural Shift

Today we transformed signup flow from:

FastAPI → DB

to:

FastAPI → Kafka → Consumer → Service → DB

This was one of the biggest backend architecture transitions till now.

---

# Topics Learned

## Kafka Topic Creation

Created:

* signup-events topic

Learned:

* partitions
* segment.bytes
* Kafka log segments
* topic persistence behavior

---

## Generic Kafka Producer Design

Refactored producer utility into reusable form:

```python
def publish_event(topic, data):
```

instead of topic-specific producer function.

Learned:

* reusable utilities
* generic architecture thinking

---

## Event Driven Architecture

Understood:

API should publish events instead of doing heavy processing directly.

New responsibility split:

### API Layer

* validate request
* publish event

### Consumer Layer

* process event
* insert into DB
* retries
* DLQ
* reliability

---

## Kafka Consumer Integration

Integrated:

* FastAPI Producer
* Kafka Topic
* Consumer
* PostgreSQL

Successfully completed:

FastAPI → Kafka → Consumer → DB flow

---

## Python Package Execution

Learned why:

```bash
python consumer.py
```

causes import problems.

Correct approach:

```bash
python -m app.kafka_client.consumer
```

Learned:

* project root execution
* package hierarchy
* Python module execution

---

## stdout Buffering

Observed:
consumer output only appearing after Ctrl+C.

Learned:

* stdout buffering
* flush=True usage

---

## Pydantic Model Reconstruction

Learned:

```python
user = UserSignup(**data)
```

Meaning:

* dict unpacking using **
* reconstruction of Pydantic objects
* reusable service layer design

---

## Architectural Thinking Improvement

Biggest learning:

Started independently thinking about:

* reusable utilities
* generic architecture
* service ownership
* event-driven processing

This marks transition from:
“learning syntax”
to:
“thinking like backend engineer”.

---

# Current Working Architecture

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
create_user()
↓
PostgreSQL

---

# Next Direction

Upcoming focus areas:

* retries
* DLQ reintegration
* idempotency
* reliability engineering
* load handling
* production-grade distributed systems
