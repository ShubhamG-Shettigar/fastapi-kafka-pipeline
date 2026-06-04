# Day 24 — Backend Architecture Interview Discussion 😄🔥

## No Coding Day

Focus:

* architecture understanding
* Kafka concepts
* interview thinking
* distributed systems reasoning

---

# Topic 1 — Why Kafka?

Discussed why systems move from:

API → DB

to:

API → Kafka → Consumer → DB

Benefits learned:

* decoupling
* asynchronous processing
* scalability
* retries
* DLQ support
* reliability

---

# Topic 2 — Event Stream vs Current State

Important distinction learned:

Kafka:

* append-only log
* event history

PostgreSQL:

* current business state
* efficient querying

Key realization:

Event Stream ≠ Current State

---

# Topic 3 — Consumer Crash Scenario

Scenario:

Consumer processes message
↓
DB insert succeeds
↓
Consumer crashes before offset commit

Problem:

* Kafka re-delivers message

Solution:

* idempotency
* unique constraints
* message IDs
* deduplication logic

---

# Topic 4 — Consumer Groups

Learned:

* group coordinator assigns partitions
* partitions distributed among consumers
* parallel processing
* consumer group scaling concepts

Important concept:

Within a consumer group,
one partition can be consumed by only one consumer at a time.

---

# Topic 5 — Offset Commit

Learned:

consumer.commit()

represents:

"Messages up to this offset have been successfully processed."

Without offset commit:

* same messages reappear
* no consumer progress occurs

---

# Topic 6 — DLQ

Purpose:

* isolate permanently failing messages
* prevent bad events from blocking healthy flow
* allow manual inspection and recovery

---

# Interview Round Scores

Q1 — DLQ
Score: 8.5/10

Q2 — Kafka vs PostgreSQL
Score: 9.5/10

Q3 — Consumer Groups
Score: 8.5/10

Q4 — consumer.commit()
Score: 9/10

Q5 — Scalable Architecture
Score: 9/10

Average:
8.9 / 10

---

# Biggest Learning

Strong shift observed from:

"What code should I write?"

to:

"How does the system behave?"

This is the beginning of backend architecture thinking.

---

# Tomorrow's Reflection Question

Topic:
Consumer Groups

Scenario:

3 partitions
5 consumers
same consumer group

Question:

How many consumers will actually do useful work?

What happens to the remaining consumers?
