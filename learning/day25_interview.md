# Day 25 - Observability Fundamentals

## Topics Covered

* Logs vs Metrics
* Production investigation flow
* Consumer lag analysis
* Kafka rebalancing
* Real-world causes of rebalancing

---

## Key Learnings

### Logs answer:

What happened?

### Metrics answer:

How much happened?

---

### Production Investigation Flow

Symptom
→ Metrics
→ Logs
→ Root Cause

Avoid jumping directly to assumptions.

---

### Consumer Lag Causes

1. Producer throughput increased
2. Insufficient consumer scaling
3. Frequent rebalancing
4. Slow consumer processing
5. Downstream dependency bottlenecks

---

### Why Rebalancing Happens

* New consumer joins
* Existing consumer leaves
* Consumer crashes
* Heartbeats stop
* Deployment / container restart
* Auto-scaling events

---

### Important Insight

Kafka does not rebalance randomly.

There is always an operational reason behind it.

---

## Current Roadmap Status

FastAPI ✅
PostgreSQL ✅
Kafka Basics ✅
Producer/Consumer ✅
Retry Logic ✅
DLQ ✅
Architecture Thinking ✅
Observability (Foundation) ✅

Next:

* Practical Observability
* Docker
* Load Testing
* Real Project
