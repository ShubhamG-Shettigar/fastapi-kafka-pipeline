# Day 31 - Interview Thinking & Failure Scenarios

## Focus

Today was intentionally lightweight.

Instead of building new features, the goal was to evaluate understanding of Kafka, distributed systems, offsets, retries, DLQ, and database correctness through interview-style scenarios.

---

# Question 1

## Scenario

Client

↓

FastAPI

↓

Kafka Topic

↓

Consumer Group

↓

PostgreSQL

Consumer behavior:

Success → Commit Offset

Failure → Retry Topic

Retry Exhausted → DLQ

Business reports duplicate records in PostgreSQL.

---

## Key Learning

Kafka provides **At-Least-Once Delivery**.

This guarantees that messages are not lost but allows messages to be processed more than once.

Therefore duplicate processing is possible.

---

## Duplicate Insert Scenario

Kafka

↓

Consumer reads message

↓

DB INSERT succeeds

↓

Consumer crashes

↓

Offset NOT committed

↓

Kafka redelivers message

↓

Consumer processes again

↓

DB INSERT again

↓

Duplicate record

---

## Important Tradeoff

### Bad Order

Kafka Offset Commit

↓

Consumer Crash

↓

DB Commit never happens

Result:

Data loss.

Kafka believes message was processed.

---

### Preferred Order

DB Commit

↓

Kafka Offset Commit

Result:

Possible duplicate processing but no message loss.

---

## Idempotency

Distributed systems should tolerate duplicate processing.

Common approach:

* Every event contains a unique identifier.
* Database enforces uniqueness.
* Duplicate events are ignored.

Example:

event_id = "abc123"

If event already exists:

* Ignore insert.
* Commit Kafka offset.
* Continue processing.

---

## Interview Keywords

* At-Least-Once Delivery
* Offset Commit
* Idempotency
* Unique Constraint
* Duplicate Processing
* Data Loss vs Duplication Tradeoff

---

# Question 2

## Scenario

Topic Partitions = 3

Consumer Group:

* consumer-1
* consumer-2
* consumer-3

consumer-2 crashes while processing a message.

Message has been fetched but offset is not yet committed.

---

## Sequence of Events

### Initial State

Partition-0 → consumer-1

Partition-1 → consumer-2

Partition-2 → consumer-3

---

### Consumer Crash

consumer-2 crashes.

Heartbeats stop.

---

### Failure Detection

Kafka detects failure using:

* session.timeout.ms
* heartbeat failures

Additionally:

* max.poll.interval.ms protects against stuck consumers.

---

### Rebalance

Group coordinator triggers rebalance.

Partition ownership is reassigned.

Example:

Partition-1

↓

consumer-3

---

### Message Reprocessing

Because offset was not committed:

Kafka assumes processing was incomplete.

Message is re-delivered.

---

### Consequence

Message may be processed twice.

Duplicate DB inserts are possible.

---

## Correct Design

Consumer reads message

↓

DB transaction

↓

Insert using unique event_id

↓

DB commit

↓

Kafka offset commit

If message is redelivered:

event_id already exists

↓

Ignore duplicate

↓

Commit offset

↓

Continue

---

## Rebalance Triggers

* Consumer joins group
* Consumer leaves group
* Consumer crash
* Topic partition count changes

---

## Heartbeats

Heartbeats inform the Group Coordinator that the consumer is alive.

Missing heartbeats beyond session timeout result in consumer removal and rebalance.

---

# Biggest Learning of Day 31

Backend systems should not be designed assuming failures will never occur.

Failures are expected:

* Consumer crashes
* Network failures
* Rebalances
* Duplicate deliveries

The objective is not preventing failures.

The objective is ensuring correctness despite failures.

This is achieved through:

* Idempotency
* Proper offset management
* Database constraints
* Retry mechanisms
* DLQ handling

A distributed system is considered reliable not because failures never happen, but because it behaves correctly when they do.
