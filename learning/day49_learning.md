# Backend Switch — Day 49 Checkpoint

## Goal

Started the **architecture refactor** of the FastAPI + Kafka + PostgreSQL backend.

The objective is to move from:

> FastAPI application that happens to use Kafka

towards:

> Event-driven backend where FastAPI is one of the producers.

---

## Project Structure

Current structure:

```text
fastapi/
│
├── app/
│   ├── configs/
│   │   └── settings.py
│   │
│   ├── db/
│   │   └── postgres.py
│   │
│   ├── kafka_client/
│   │   ├── consumer.py
│   │   └── producer.py
│   │
│   ├── models/
│   │   └── schemas.py
│   │
│   ├── routes/
│   │   └── auth_routes.py
│   │
│   ├── services/
│   │   ├── auth_service.py
│   │   └── retryhandler.py
│   │
│   ├── main.py
│   └── metrics.py
│
├── prometheus.yml
│
└── kafka/
    └── Kafka 3.7.0 binaries
```

Backup exists:

```text
app_backup_day48/
```

---

# Work Completed

## 1. `settings.py` — Refactored

Created a centralized configuration object using Pydantic Settings.

Current responsibilities:

* Application configuration
* Kafka configuration
* PostgreSQL configuration
* `.env` support

Important configuration:

```text
kafka_bootstrap_servers = localhost:9092
kafka_orders_topic = orders
kafka_retry_topic = orders-retry
kafka_dlq_topic = orders-dlq

postgres_host = localhost
postgres_port = 5432
postgres_db = kafka_project
postgres_user = postgres
postgres_password = postgresql
```

We intentionally use lowercase attributes.

Understanding:

```text
Settings = configuration blueprint
settings = actual configuration object
```

Also understood the purpose of:

```python
class Config:
    env_file = ".env"
```

It allows Pydantic Settings to read configuration from `.env`.

---

## 2. `postgres.py` — Refactored

Old implementation had:

* Hardcoded DB configuration
* Global PostgreSQL connection
* Global cursor
* Automatic table creation during module import

New implementation:

```text
settings.py
     ↓
postgres.py
     ↓
PostgreSQL
```

Main functions:

```text
get_connection()
get_db()
get_cursor()
```

`get_connection()`:

* Creates a PostgreSQL connection using centralized settings.

`get_db()`:

* Creates connection
* Creates cursor
* Uses `yield`
* Cleans up cursor and connection using `finally`

Important concept learned:

```text
Connection = communication channel with PostgreSQL

Cursor = interface used to execute SQL
```

Also understood that multiple applications can use the same PostgreSQL database, but normally each application/process maintains its own DB connections rather than sharing one connection object.

Table creation was intentionally removed from module import behaviour.

---

## 3. `producer.py` — Refactored

Kafka producer now uses centralized settings.

Old hardcoded configuration was removed.

Current producer concept:

```text
Application
    ↓
publish_event()
    ↓
KafkaProducer
    ↓
Kafka
```

Producer supports an optional topic:

```python
publish_event(data)
```

uses the default:

```text
orders
```

while:

```python
publish_event(data, topic)
```

can explicitly publish to another topic.

This is needed for:

```text
orders
orders-retry
orders-dlq
```

Producer reliability topics such as:

* `acks`
* retries
* idempotence
* ordering
* batching

are intentionally postponed to Phase 2.

---

## 4. `schemas.py` — Refactored

Existing API models were retained:

```text
UserSignup
UserLogin
User
MessageResponse
```

Added:

```text
EventEnvelope
```

Concept:

```text
EventEnvelope
├── event_id
├── event_type
├── event_version
├── timestamp
├── source
└── payload
```

Current payload:

```python
payload: dict[str, Any]
```

This is an initial foundation for future:

* Complex events
* Nested payloads
* Multiple event types
* Event versioning
* Schema Registry

We are intentionally not over-engineering the event schema yet.

---

## 5. `retryhandler.py` — Created

Previously this file was empty.

It now handles:

```text
Failed event
    ↓
Check retry_count
    ↓
retry available?
 ├── YES → retry topic
 └── NO  → DLQ
```

Current:

```text
MAX_RETRIES = 1
```

Metrics are also updated:

```text
retry_events_total.inc()
dlq_events_total.inc()
```

Important discovery:

The current retry architecture is **not complete yet**.

Because events are being moved to:

```text
orders-retry
```

but the current consumer only consumes:

```text
orders
```

Therefore the retry event does not currently return to the processing flow.

This needs to be addressed before considering the retry architecture complete.

---

## 6. `consumer.py` — Started Refactor

Old consumer had too many responsibilities:

```text
Kafka consumption
Producer creation
PostgreSQL
User creation
Retry
DLQ
Metrics
Prometheus server
Failure simulation
Offset commits
```

New consumer was simplified toward:

```text
Kafka
  ↓
Consumer
  ↓
Process event
  ↓
Success → metric → commit

Failure
  ↓
retryhandler
```

Current consumer:

* Uses centralized Kafka settings
* Consumes `orders`
* Uses consumer group `orders_group`
* `enable_auto_commit=False`
* Uses JSON deserialization
* Calls `processed_events_total.inc()` on successful processing
* Commits offset after successful processing
* Calls `handle_failure()` on processing failure

DB processing has intentionally NOT been added yet.

---

# Important Architecture Decisions

## Clear module responsibilities

```text
settings.py
→ configuration

postgres.py
→ PostgreSQL connection/access

producer.py
→ Kafka publishing

schemas.py
→ API/event models

consumer.py
→ Kafka consumption + processing flow + offset management

retryhandler.py
→ retry/DLQ handling

auth_service.py
→ authentication/security

auth_routes.py
→ HTTP/API endpoints

main.py
→ FastAPI application entry point

metrics.py
→ Prometheus metric definitions
```

We explicitly decided **not** to create unnecessary enterprise-style layers/classes.

---

# Files Still To Refactor

```text
auth_service.py
auth_routes.py
main.py
metrics.py
```

`metrics.py` is already relatively clean and may require only minor/no changes.

---

# Important Current State

```text
settings.py       ✅
postgres.py       ✅
producer.py       ✅
schemas.py        ✅
retryhandler.py   🟡 Started
consumer.py       🟡 Started
auth_service.py   ⏳
auth_routes.py    ⏳
main.py           ⏳
metrics.py        ✅ / minor review
```

Kafka broker:

```text
RUNNING
```

Uvicorn:

```text
STOPPED
```

Consumer:

```text
STOPPED
```

Prometheus/Grafana:

```text
NOT RUNNING
```

---

# Key Learning From Day 49

The main lesson was not just moving code between files.

We started separating **responsibilities**:

```text
Configuration
     ↓
Infrastructure
     ↓
Kafka
     ↓
Processing
     ↓
Business logic
     ↓
Persistence
```

We also identified an important design issue:

> A Kafka retry topic is not useful by itself. Something must consume/process that retry topic and bring the event back into the processing flow or handle it appropriately.

This will be resolved before the new architecture is considered complete.

---

# Next Session

Continue the Phase 1 refactor.

Priority:

1. Finalize retry architecture.
2. Complete `consumer.py`.
3. Refactor `auth_service.py`.
4. Refactor `auth_routes.py`.
5. Clean `main.py`.
6. Review `metrics.py`.
7. Start all components.
8. Test the complete flow end-to-end.
9. Establish a fresh working baseline.

Only after the baseline is stable will we move to:

```text
Phase 2 → Kafka Producer Reliability
```

with:

```text
acks
retries
idempotent producer
ordering
batching
```
