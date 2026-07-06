# Day 47 - Interview Practice

## Scenario

A Kafka consumer exposes the following Prometheus metrics:

* processed_events_total
* retry_events_total
* dlq_events_total

At **10:00 AM**, an alert is received:

> "Signup processing is delayed."

Grafana dashboard observations:

* processed_events_total → Flat
* retry_events_total → Flat
* dlq_events_total → Flat

Kafka producers are healthy and continue producing new messages.

---

# Question 1

### How would you debug this issue?

### My Answer

Since new Kafka messages are being produced but none of the counters are increasing, the issue is likely between the consumer polling records and successfully processing/committing them.

Possible reasons include:

* Consumer process has crashed.
* Consumer is unable to poll Kafka.
* Database or downstream dependency is blocking processing.
* Offset commits are not happening.

### Improved Interview Answer

A structured debugging approach:

1. Verify that the consumer process is running.
2. Check consumer logs for exceptions or crashes.
3. Verify that the consumer is polling records from Kafka.
4. Check downstream dependencies (Database/API).
5. Verify offset commits.
6. Check consumer lag.
7. Correlate observations with Prometheus metrics.

Only after collecting evidence should the root cause (for example, a DB bottleneck) be concluded.

---

# Question 2

### Prometheus also shows no metric updates.

How do you determine whether the problem is Consumer, Prometheus or Grafana?

### My Answer

Since the consumer exposes the metrics, the problem is likely in the consumer.

### Improved Interview Answer

Since Prometheus itself is not showing updated values, Grafana is ruled out.

Next step:

* Open the consumer's `/metrics` endpoint directly.
* If `/metrics` values are stale, the issue lies within the consumer.
* If `/metrics` is updating correctly but Prometheus is not reflecting the changes, investigate Prometheus scraping configuration or target health.

---

# Question 3

### Why is Prometheus required between the application and Grafana?

### My Answer

Prometheus scrapes metrics from the application, stores them as time-series data, and executes PromQL queries. Grafana sends PromQL queries to Prometheus and visualizes the returned data.

### Interview Enhancement

Prometheus provides:

* Time-series database
* Metric scraping
* Historical storage
* PromQL query engine

Without Prometheus, Grafana would have to scrape `/metrics` directly, resulting in:

* No historical data
* No PromQL support
* No centralized metric collection across multiple services

---

# Learning

Interviewers usually evaluate the debugging approach more than the final answer.

A good debugging sequence is:

Observe → Verify → Isolate → Conclude

Avoid jumping directly to a root cause without first collecting evidence.

---

# Progress

Current Observability Journey:

✅ Prometheus Metrics

✅ PromQL Basics

✅ Counters & Gauges

✅ Rate() & Increase()

✅ Grafana Installation

✅ First Dashboard

✅ Multi-Series Visualization

⏳ Grafana Login Investigation (Pending)

⏳ Labels

⏳ Aggregation using `by()`

⏳ Dashboard Customization

⏳ Histograms

---

# Reminder for Next Session

1. Resolve Grafana login issue properly.
2. Continue from existing dashboard.
3. Deep dive into Labels.
4. Learn `sum by(...)` and other aggregation operators.
5. Continue building a production-style dashboard.
