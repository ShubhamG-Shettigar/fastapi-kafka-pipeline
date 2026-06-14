# Day 33 — Production Incident Round

Theme:
Transition from building systems → debugging systems.

Focus:
Failure → Impact → Recovery → Correctness

---

## Incident 1 — Consumer Lag Suddenly Jumps

### Symptoms

Producer Rate:
10,000 msgs/min

Consumer Rate:
10,000 → 2,000 msgs/min

DB Query Time:
20ms → 850ms

Active Connections:
95/100

Kafka Healthy

### Root Cause

Consumer throughput reduced because DB became bottleneck.

Flow:

Consumer
↓
DB Write Slow
↓
Processing Time Increases
↓
Throughput Drops
↓
Kafka Lag Increases

### Learning

Consumer Lag ≠ Kafka Problem

Investigate entire processing path.

---

## Incident 2 — Missing Messages

### Symptoms

Produced:
10,000

Consumed:
10,000

DB Rows:
9,820

Missing:
180

Auto Commit:
true

### Root Cause

Offset committed before successful business processing.

Flow:

Read Message
↓
Offset Auto Commit
↓
DB Insert Fails
↓
Consumer Restarts
↓
Kafka Starts From Next Offset

Message Lost

### Learning

Consumed ≠ Successfully Processed

Manual offset commit after successful business processing.

---

## Incident 3 — Phantom Rebalance

### Symptoms

Frequent:

Partitions Revoked
Partitions Assigned

Lag Oscillation:
0 → 50k → 0 → 40k

Recent Change:

max.poll.records

500 → 5000

### Root Cause

Large batch processing increased processing time.

Consumer exceeded:

max.poll.interval.ms

Kafka assumed consumer was stuck and triggered rebalance.

### Learning

Heartbeats alone do not guarantee consumer health.

More records per poll can reduce throughput.

---

## Incident 4 — Retry Storm

### Symptoms

Payment Service Response Time:

200ms → 8-10 sec

Consumer Lag:
0 → 200k

Request Rate:
100/sec → 1200/sec

Retries:
5 (Immediate)

### Root Cause

Slow downstream service triggered retry amplification.

Flow:

Slow Service
↓
Timeout
↓
Immediate Retry
↓
More Load
↓
More Timeouts
↓
More Retries

Retry Storm

### Learning

Recovery mechanisms can amplify failures.

Mitigations:

- Exponential Backoff
- Circuit Breaker
- Retry Limits
- DLQ

---

## Incident 5 — Out-of-Order Events

### Scenario

Account Events:

Credit +100
Debit -50

Expected Balance:
50

Actual:
-50

### Root Cause

Related events landed in different partitions.

Debit processed before Credit.

### Learning

Kafka guarantees:

Ordering Within A Partition

Not:

Ordering Across Partitions

Fix:

Partition Key = accountId

Ensures all account events reach same partition.

---

## Key Concepts Reinforced

- Consumer Lag Investigation
- Offset Management
- Auto Commit Risks
- At-Least-Once Delivery
- Duplicate Processing
- Idempotency
- Rebalances
- max.poll.interval.ms
- Retry Storms
- Circuit Breakers
- Exponential Backoff
- DLQ
- Event Ordering
- Partitioning Strategy

---

## Biggest Learning

Do not jump directly to Kafka.

Investigate:

Client
↓
API
↓
Consumer
↓
DB
↓
Kafka

Symptoms point to affected components.

Metrics reveal root cause.

Evidence before conclusions.