# Day 34 — Rapid Revision + Distributed Systems Correctness

## Rapid Revision

### Kafka Consumer Crash After DB Commit

Scenario:

DB Commit Success
↓
Consumer Crash
↓
Offset Not Committed

Learning:

* Kafka provides At-Least-Once delivery.
* Message will be reprocessed.
* Duplicate business operations can occur.
* Idempotency is required at the business/DB layer.

Common Fix:

* Idempotency Key
* Unique Business Identifier
* Processed Event Table

---

### API Latency Investigation

Question:

API latency jumps from 200ms to 3 seconds.

Investigation Order:

1. Logs
2. Metrics
3. Distributed Tracing

Check:

* CPU
* Memory
* DB Connections
* Query Latency
* Downstream Dependencies
* Error Rates

Learning:

Investigate before forming hypotheses.

---

### max.poll.records vs max.poll.interval.ms

max.poll.records

* Number of records returned in one poll.

max.poll.interval.ms

* Maximum allowed time between two poll() calls.

Failure Scenario:

Increase:

500 → 5000 records

Processing time increases.

Consumer exceeds:

max.poll.interval.ms

Kafka assumes consumer is stuck.

Rebalance occurs.

Learning:

Higher batch size can reduce throughput.

---

### Retry Storm

Problem:

Slow downstream service.

Retries happen immediately.

Result:

More load
↓
More timeouts
↓
More retries
↓
Retry Storm

Mitigations:

* Exponential Backoff
* Circuit Breaker
* Retry Limits
* DLQ

Learning:

Recovery mechanisms can amplify failures.

---

### Kafka Ordering

Kafka guarantees ordering:

ONLY within a partition.

Ordering breaks when:

* Related events land in different partitions.

Fix:

Use partition key.

Example:

accountId
orderId
userId

Learning:

Ordering is a partition-level guarantee.

---

## Challenge Question — Payments Under Uncertainty

Architecture:

Producer
↓
Kafka
↓
Consumer
↓
Payment Gateway
↓
DB

Goal:

* No lost payments
* No duplicate payments

---

### Idempotency Key

Generate:

payment_request_id

Pass it through all layers.

Benefits:

* Safe retries
* Duplicate suppression
* Replay protection

---

### Distributed Systems Uncertainty

Scenario:

DB Commit Success
↓
Network Partition
↓
Response Lost

Consumer sees:

"Maybe Failed"

Reality:

"Maybe Succeeded"

Learning:

Consumer cannot distinguish:

* Failure
* Success with lost response

This is a fundamental distributed systems problem.

---

### Why UNIQUE(order_id) Is Not Always Enough

Scenario:

Payment Gateway Charges Customer
↓
Application Crashes
↓
DB Write Never Happens

Result:

DB contains no record.

UNIQUE(order_id) cannot help because no row exists.

Learning:

Database is not always the source of truth.

---

### Authoritative Source Principle

Question:

Customer charged?

DB says:
Unknown

Kafka says:
Unknown

Consumer says:
Unknown

Solution:

Query the authoritative source.

Example:

Payment Gateway

Check status using:

payment_request_id

Response:

* SUCCESS
* FAILED
* PENDING

Learning:

When system state is uncertain, query the authoritative system.

---

## Biggest Learning Of The Day

A system can be in a state where:

Maybe Success
Maybe Failure

And the application genuinely cannot know.

Distributed systems are often about handling uncertainty rather than preventing all failures.

The correct response is not guessing.

The correct response is reconciliation using an authoritative source.
