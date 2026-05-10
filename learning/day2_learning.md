# Day 2 Learning 🚀

## 📌 Topics Covered

- Kafka offset commit behavior (manual commit enabled)
- Difference between auto commit and manual commit
- At-least-once delivery semantics in Kafka
- Consumer crash scenarios and message reprocessing
- DB duplication problem due to missing offset commit
- Sync commit concept (blocking commit behavior)
- Git Bash vs Windows CLI path issues in Kafka setup

---

## ⚙️ Key Experiments Performed

### 1. Consumer Crash Before Commit
- Inserted message via FastAPI → Kafka → Consumer
- DB insert completed
- Consumer was killed before Kafka offset commit
- Result: same message reprocessed after restart → DB duplicates observed

---

### 2. Kafka Commit vs DB Commit Understanding
- Kafka does NOT know DB state
- Offset commit decides message re-delivery
- Ordering impacts:
  - DB → Kafka commit → duplicates possible
  - Kafka commit → DB → data loss possible

---

### 3. Manual Offset Commit Enabled
- Disabled auto commit
- Implemented explicit `consumer.commit()`
- Observed controlled offset behavior

---

## 🧠 Key Learnings

- Kafka guarantees **at-least-once delivery, not uniqueness**
- Duplicate processing is expected in failure scenarios
- Offset commit timing is critical for correctness
- Idempotency is required for production systems
- Kafka + DB consistency must be designed, not assumed

---

## ⚠️ Infrastructure Issue Solved

### KRaft Broker Failure

Issue:
- `meta.properties not found`
- `AccessDeniedException`
- `kraft-combined-logs corruption`

Fix: Run inside kafka folder
```bash
a. bin/kafka-storage.sh random-uuid 
b. bin/kafka-storage.sh format -t <uuid> -c config/kraft/server.properties