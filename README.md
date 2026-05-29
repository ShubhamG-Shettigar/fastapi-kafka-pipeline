# FastAPI Kafka Pipeline 🚀

A scalable event-driven backend system built using:

* FastAPI
* Apache Kafka
* PostgreSQL
* JWT Authentication

---

# Current Architecture

Client → FastAPI → Kafka Producer → Partitioned Kafka Topic → Consumer Group → PostgreSQL

---

# Current Features

## Backend Features

* JWT-based authentication
* User signup/login APIs
* Protected API routes
* Modular FastAPI architecture
* Dependency Injection (`Depends`)
* Middleware fundamentals
* Async request handling basics

---

## Kafka Features

* Kafka producer/consumer integration
* Manual offset commits
* Multi-consumer scaling
* Consumer group rebalancing experiments
* Partition-based parallel processing
* Idempotent consumer handling

---

## Database Features

* PostgreSQL persistence
* Secure password hashing
* Transaction handling basics
* Connection/cursor lifecycle understanding

---

# Key Concepts Implemented

## Backend Concepts

* Request lifecycle
* Middleware basics
* Dependency Injection
* JWT token verification
* Async vs sync processing
* Blocking vs non-blocking IO

---

## Distributed Systems Concepts

* At-least-once semantics
* Idempotent event processing
* Kafka consumer groups
* Sticky partitioning
* Partition ownership and rebalancing
* Distributed event consumption

---

# Future Vision

* Refresh token implementation
* Retry mechanism
* Dead Letter Queue (DLQ)
* SQLAlchemy integration
* Async database handling
* Dockerization
* Load testing
* Monitoring and observability
* Kubernetes deployment
* Production-grade distributed backend system

---

# Learning Goals

This project is focused on learning:

* backend engineering fundamentals
* distributed systems
* event-driven architecture
* scalable microservice patterns
* production-oriented backend design
