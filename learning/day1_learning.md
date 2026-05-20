# Day 1 Learning Notes 🚀

## Topics Covered

- Kafka setup in KRaft mode
- Topic creation and partitions
- Producer and consumer basics
- Consumer groups and offsets
- FastAPI integration with Kafka
- SQLite database integration
- JSON serialization and deserialization
- Pydantic request validation
- Logging basics in Python consumer
- Retry and reprocessing concepts
- At-least-once processing semantics

---

## Important Learnings

### Kafka stores bytes, not objects
Data must be serialized before sending and deserialized after consuming.

### Offset commits are important
Consumer continues from the last committed offset after restart.

### FastAPI validation happens before Kafka
Invalid request payloads are rejected by Pydantic itself.

### Internal Kafka topics exist
Kafka internally uses topics like:
__consumer_offsets

### Infra issues vs application issues
Kafka broker failures can happen independently from application code.

---

## Real Issue Faced

### Kafka Broker Failure

Issue:
Kafka broker shutdown with:
all log dirs have failed

Root Cause:
Windows file lock issue on Kafka internal offset topic files.

Fix:
- Removed stale lock files (.lock inside kafka folder)
- Deleted corrupted __consumer_offsets-* folders
- Restarted broker cleanly
- Format storage command to freshly create kraft-combined-logs
Run inside kafka folder
```bash
a. bin/kafka-storage.sh random-uuid 
b. bin/kafka-storage.sh format -t <uuid> -c config/kraft/server.properties
---

## Overall Understanding

Current pipeline working successfully:

Client
→ FastAPI
→ Kafka Producer
→ Kafka Broker
→ Kafka Consumer
→ SQLite DB