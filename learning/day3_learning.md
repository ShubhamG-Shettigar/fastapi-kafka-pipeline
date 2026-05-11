# Day 3 Learning 🚀

## Topics Covered
- Idempotent consumer design
- Duplicate-safe Kafka processing
- Message identity using message_id
- DB uniqueness constraint handling

---

## Practical Work Done

### 1. Added message_id
- FastAPI now generates UUID-based message_id
- Event identity travels through Kafka pipeline

### 2. Added DB Uniqueness
- SQLite table updated with:
  - message_id TEXT UNIQUE
- Prevents duplicate inserts

### 3. Crash Simulation
Scenario:
- DB insert completed
- Consumer crashed before Kafka commit
- Kafka re-delivered same message after restart

Result:
- Duplicate DB insert prevented successfully
- Existing message_id rejected by DB

---

## Key Learning

Kafka duplicates cannot always be prevented.

Real systems solve this using:
- Idempotent consumer design
- Unique event/message identifiers
- DB-level duplicate protection