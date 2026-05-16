# FastAPI Kafka Pipeline 🚀

A scalable event-driven backend system built using:

* FastAPI
* Apache Kafka
* PostgreSQL

---

## Current Architecture

FastAPI → Kafka Producer → Partitioned Kafka Topic → Consumer Group → PostgreSQL

---

## Current Features

* Event-driven API architecture
* Kafka producer/consumer integration
* Manual offset commits
* Idempotent consumer handling
* PostgreSQL persistence
* Multi-consumer scaling
* Consumer group rebalancing experiments
* Partition-based parallel processing

---

## Key Concepts Implemented

* At-least-once semantics
* Idempotent event processing
* Kafka consumer groups
* Sticky partitioning
* Partition ownership and rebalancing
* Distributed event consumption

---

## Future Vision

* Retry mechanism
* Dead Letter Queue (DLQ)
* Dockerization
* Load testing
* Monitoring and observability
* Kubernetes deployment
* Production-grade distributed backend system
