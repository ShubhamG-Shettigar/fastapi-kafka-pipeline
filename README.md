# FastAPI Kafka Pipeline 🚀

A scalable event-driven backend system built using:

* FastAPI
* Apache Kafka
* PostgreSQL
* JWT Authentication
* Prometheus Metrics

---

# Current Architecture

Client → FastAPI → Kafka Producer → Partitioned Kafka Topic → Consumer Group → PostgreSQL

Observability Flow:

Consumer → Prometheus Metrics Endpoint → (Future: Prometheus Server → Grafana)

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
* Retry mechanism
* Dead Letter Queue (DLQ)

---

## Database Features

* PostgreSQL persistence
* Secure password hashing
* Transaction handling basics
* Connection/cursor lifecycle understanding
* Rollback handling

---

## Observability Features

* Prometheus Counter metrics
* Prometheus Gauge metrics
* Consumer metrics endpoint exposure
* Consumer observability foundation
* Consumer lag monitoring foundation

Metrics implemented:

* processed_events_total
* retry_events_total
* dlq_events_total
* consumer_lag

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

* At-least-once delivery semantics
* Idempotent event processing
* Kafka consumer groups
* Sticky partitioning
* Partition ownership
* Consumer group rebalancing
* Distributed event consumption
* Retry workflows
* Dead Letter Queue design

---

## Observability Concepts

* Logs vs Metrics vs Traces
* Counter vs Gauge
* Metrics exposure
* Metrics scraping architecture
* Consumer lag monitoring concepts
* Prometheus fundamentals
* Observability ownership principle

---

# Future Vision

## Observability

* Prometheus server integration
* Grafana dashboards
* Distributed tracing
* Business metrics dashboards

---

## Backend

* Refresh token implementation
* SQLAlchemy ORM migration
* Async database handling
* Background task processing
* API rate limiting

---

## Infrastructure

* Dockerization
* Load testing
* CI/CD basics
* Kubernetes deployment
* Production-grade distributed backend system

---

# Learning Goals

This project is focused on learning:

* Backend Engineering Fundamentals
* Distributed Systems
* Event-Driven Architecture
* Scalable Microservice Patterns
* Observability
* Production-Oriented Backend Design

---

# Roadmap Progress

* FastAPI ✅
* JWT Authentication ✅
* PostgreSQL ✅
* Kafka Producer/Consumer ✅
* Retry Mechanism ✅
* DLQ ✅
* Observability Foundations ✅
* Prometheus Metrics Exposure ✅
* Prometheus Scraping ⏳
* Grafana Dashboards ⏳
* Docker ⏳
* SQLAlchemy ⏳
* Testing ⏳
* Kubernetes ⏳
