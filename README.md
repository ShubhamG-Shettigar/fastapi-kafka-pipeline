# FastAPI + Kafka Pipeline 🚀

A learning-based backend project to understand real-world Kafka behavior using FastAPI, Python consumers, and database integration.

---

## 📌 Architecture
Client
↓
FastAPI (API Layer)
↓
Kafka Producer
↓
Kafka Broker (KRaft mode)
↓
Python Consumer
↓
SQLite Database


---

## ⚙️ Current State

- FastAPI endpoint to publish messages to Kafka
- Kafka producer-consumer pipeline working
- Python consumer processing messages and storing in SQLite DB
- Manual offset commit implemented
- Experiments done on consumer crash and message reprocessing

---

## 🧠 Focus Area (Current Learning)

- Kafka offset commit behavior (manual vs auto)
- At-least-once delivery understanding
- Consumer crash recovery scenarios
- Handling duplicate message processing

---

## 🚀 Future Vision

- Implement idempotent consumer design (no duplicate DB writes)
- Improve reliability patterns (production-grade Kafka handling)
- Explore async vs sync commit strategies
- Add scalable multi-consumer setup
- Containerize system using Docker