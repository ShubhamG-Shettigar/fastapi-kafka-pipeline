# Day 32 — Production Incident Round

## Incident 1: Max Poll Interval Exceeded

### Scenario

Consumer exceeds `max.poll.interval.ms` due to slow processing.

### Root Cause

Consumer reads from Kafka quickly, but processing involves:

* DB calls
* External APIs
* Network operations
* File/Cache access

If processing takes too long, consumer doesn't call `poll()` within the configured interval.

### Impact

* Kafka assumes consumer is stuck
* Rebalance occurs
* Partitions get reassigned
* Potential lag spike

### Key Learning

Kafka consumption is fast; business processing is often the bottleneck.

---

## Incident 2: Payment Duplication ("The Dangerous Success")

### Symptoms

* Users charged twice
* No alerts
* No deployment
* Kafka healthy
* DB healthy

### Initial Wrong Hypothesis

Kafka duplicates / Producer retries / Missing transactions.

### Critical Clue

Users experience slow response and press "Pay" again.

### Actual Flow

User clicks Pay
→ Response delayed
→ User clicks Pay again
→ API receives two valid requests
→ No idempotency check
→ Both payments succeed

### Root Cause

Correctness failure, not infrastructure failure.

### Immediate Mitigation

* Block duplicate payments for already successful orders
* Refund affected customers

### Long-Term Fix

Implement idempotency.

Example:

if orderId exists AND status = SUCCESS
reject duplicate request

### Key Learning

Duplicates may originate before Kafka ever sees the request.

Always investigate from:
Client → API → DB → Kafka

Don't assume Kafka is guilty first.
