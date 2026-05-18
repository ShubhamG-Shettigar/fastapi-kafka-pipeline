# Day 9 - Advanced Distributed Systems Interview Reasoning

## Scenario

Architecture:

Frontend
↓
FastAPI
↓
Kafka
↓
Consumer Group
↓
PostgreSQL

Traffic spike:
100 req/sec → 25,000 req/sec

Observed problems:

* Kafka lag increasing
* retries increasing
* PostgreSQL CPU at 95%
* DLQ traffic increasing
* autoscaling worsening instability
* duplicate notifications observed

---

# Key Learning

Distributed systems problems are often:

* bottleneck propagation problems
* not isolated component failures

---

# 1. Primary Bottleneck Identification

Observed:

* PostgreSQL CPU at 95%
* autoscaling consumers worsened system

Inference:

* Database is likely primary bottleneck

Reason:
Increasing consumers increased:

* DB writes
* retries
* connection pressure
* contention

Kafka itself was not necessarily the limiting component.

---

# 2. Why Autoscaling Consumers Can Worsen System

More consumers:

* increase parallel DB operations
* increase retry traffic
* increase connection pool usage
* increase lock contention

If DB cannot handle additional throughput:
system instability worsens.

Important:
Scaling consumers without scaling downstream dependencies can amplify failures.

---

# 3. Duplicate Business Actions

Even with DB idempotency:
duplicate side-effects can occur.

Example:

* notification/email/payment executed
* consumer crashes before offset commit
* Kafka replays event
* side-effect executes again

Important:
DB idempotency alone does not guarantee external side-effect idempotency.

---

# 4. Important Metrics To Observe

## Kafka Metrics

* consumer lag
* partition throughput
* rebalance frequency

## PostgreSQL Metrics

* CPU usage
* query latency
* connection pool saturation
* lock contention

## Application Metrics

* retry count
* DLQ growth
* API latency
* request throughput

---

# 5. Stabilization Strategies

Possible immediate mitigations:

* producer-side rate limiting
* exponential backoff
* temporary traffic throttling
* isolate retry traffic
* reduce retry aggressiveness
* circuit breaker patterns

Goal:
protect downstream systems from cascading failures.

---

# 6. Why Partitions Alone May Not Solve Issue

More partitions:

* improve Kafka parallelism

BUT:
if DB remains bottleneck,
additional consumers can worsen:

* DB pressure
* retries
* contention

Scaling must happen across entire pipeline.

---

# 7. Long-Term Architectural Improvements

Potential improvements:

* retry topics
* exponential backoff
* batching
* connection pooling
* DB indexing
* caching
* circuit breakers
* async processing
* load shedding
* read replicas
* query optimization

---

# Important Distributed Systems Principle

Reliable systems are not systems where failures never happen.

Reliable systems are systems where failures are safely contained and managed.
