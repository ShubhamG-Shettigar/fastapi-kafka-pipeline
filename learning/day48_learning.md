# Day 48 – Backend Switch (Kafka Re-entry)

## Objective

Resume the Backend Switch practicals after a long break by rebuilding the Kafka mental model through hands-on experiments and preparing the project for deeper event-driven architecture.

---

## Today's Work

Recovered the existing flow:

```text
FastAPI → Producer → signup-events → Consumer → PostgreSQL
                              ↓
                         Retry / DLQ