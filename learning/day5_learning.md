# Day 5 Learning 🚀

## Topics Covered
- Kafka replay vs application retry
- Offset-based message reprocessing
- PostgreSQL fundamentals
- Relational database systems overview

---

## Kafka Learning

### Replay vs Retry Understanding

Initially, replay behavior was interpreted as:
- Kafka automatically retrying/redelivering messages

Further debugging clarified the actual behavior:

- Kafka consumers continuously poll messages
- Kafka only tracks committed offsets
- If offset is not committed, the same message remains available for future polling

This means:
- Replay happens because consumer polls again from the last committed offset
- Kafka is not actively retrying business logic

---

## Key Distributed Systems Insight

Kafka does not know:
- whether DB insert succeeded
- whether business logic completed

Kafka only knows:
- which offset was committed by the consumer

Therefore:
- same message may be processed multiple times until offset commit happens

---

## PostgreSQL Introduction

Started migration planning from:
- SQLite → PostgreSQL

Learned:
- SQL is a query language
- PostgreSQL is a database server system implementing SQL
- pgAdmin is a GUI management tool for PostgreSQL
- EnterpriseDB (EDB) provides Windows installer distribution

---

## Practical Work Done

- Began PostgreSQL installation setup
- Investigated pgAdmin startup issue
- Verified missing PostgreSQL service
- Planned clean reinstall procedure

---

## Key Learning

Distributed systems correctness depends heavily on:
- offset semantics
- idempotent processing
- accurate mental models of replay behavior

Understanding protocol behavior is more important than memorizing definitions.