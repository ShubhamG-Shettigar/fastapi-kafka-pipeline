# Day 8 - Interview Notes

## Q1. Difference between consumer crash and processing failure

Consumer crash:

* process dies
* Kafka replays uncommitted messages
* requires restart

Processing failure:

* consumer stays alive
* application retry logic handles failure

---

## Q2. Why are retries implemented using new Kafka events?

Because Kafka is append-only.

Retries are generally handled through:

* republishing retry events
* not modifying old offsets/messages

This improves replay safety and operational control.

---

## Q3. Why is idempotency important?

Kafka systems can produce duplicates because of:

* retries
* offset resets
* rebalances
* consumer restarts

Idempotent processing ensures:

* duplicate events do not corrupt business state

Implemented using:

* UUID UNIQUE constraint in PostgreSQL

---

## Q4. What is a DLQ?

Dead Letter Queue stores messages that:

* failed repeatedly
* require manual handling
* should not block pipeline

DLQ prevents:

* infinite retry loops
* retry storms
* consumer blockage

---

## Q5. Why can aggressive retries be dangerous?

Aggressive retries can create:

* retry storms
* cascading failures
* increased lag
* CPU spikes
* DB overload

Retries themselves become additional producer traffic.

---

## Q6. Will increasing Kafka partitions always improve throughput?

No.

If downstream DB is bottleneck:

* more consumers can worsen DB pressure

Need:

* bottleneck identification
* controlled scaling
* indexing
* retry management

---

## Q7. What causes consumer lag?

Consumer lag occurs when:

* message production rate >
  processing throughput

Reasons:

* slow DB
* retries
* downstream failures
* heavy processing

---

## Q8. Difference between retryable and non-retryable errors

Retryable:

* DB timeout
* network issue
* temporary API failure

Non-retryable:

* invalid payload
* schema mismatch
* corrupted data

Non-retryable errors usually go directly to DLQ.
