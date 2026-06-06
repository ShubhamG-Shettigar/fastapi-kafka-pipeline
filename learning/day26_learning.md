# Day 26 - Observability Practical

## Topics Covered

### 1. Python Package Imports

Project should be executed consistently from project root.

Correct startup commands:

```bash
uvicorn app.main:app --reload
python -m app.kafka_client.consumer
```

Use absolute imports everywhere:

```python
from app.db.postgres import conn
from app.services.auth_service import create_user
from app.models.schemas import UserSignup
```

Avoid mixing:

```python
from db.postgres import conn
```

and

```python
from app.db.postgres import conn
```

---

### 2. Logging vs Print

Migrated consumer from basic prints to structured logging.

Used:

```python
logging.info()
logging.warning()
logging.error()
```

Important:

```python
print(..., flush=True)
```

is valid.

```python
logging.info(..., flush=True)
```

is invalid and causes:

```text
Logger._log() got an unexpected keyword argument 'flush'
```

---

### 3. Meaningful Consumer Logs

Implemented logs for:

* Consumer startup
* Event received
* User inserted successfully
* Retry attempts
* DLQ movement
* Offset commits

---

### 4. Basic Metrics Counters

Implemented:

```python
processed_count
retry_events
dlq_events
```

Displayed after every event:

```python
Stats => processed=X, retries=Y, dlq=Z
```

---

### 5. Observability Flow

Application
→ Logs
→ Metrics
→ Monitoring

---

### 6. Success / Retry / DLQ Testing

Verified:

* Success path
* Retry path
* DLQ path

Logs and counters behaved correctly.

---

### 7. Why Counters Reset After Restart

Kafka stores:

* Consumer Group ID
* Offsets

Kafka does NOT store:

```python
processed_count
retry_events
dlq_events
```

These are in-memory variables.

Restarting consumer:

```text
Offsets retained
Counters reset
```

---

### 8. Time-Series Database Concept

Metrics are usually stored externally.

Typical flow:

Application
→ Prometheus
→ Time-Series Database
→ Grafana Dashboard

Purpose:

Store historical metric values with timestamps.

Example:

```text
10:00 -> processed = 100
10:01 -> processed = 120
10:02 -> processed = 150
```

This data survives application restarts.

---

## Current Progress

FastAPI ✅
PostgreSQL ✅
Kafka Basics ✅
Producer/Consumer ✅
Retry Logic ✅
DLQ ✅
Architecture Thinking ✅
Observability Fundamentals ✅
Observability Practical Basics ✅

Next:

* ELK
* Prometheus
* Grafana
* Real Monitoring Concepts
