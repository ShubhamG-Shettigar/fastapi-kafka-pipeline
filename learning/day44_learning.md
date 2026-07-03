# Day 33 – Backend Switch

## Duration

~45 minutes

---

## Revision Completed

### Architecture Revision

Ports understood clearly:

* **8000** → FastAPI (Uvicorn)
* **8001** → Metrics endpoint exposed by the consumer process (`start_http_server(8001)`)
* **9090** → Prometheus Server

Important clarification:

`localhost:8001` is **not** another consumer instance. It is a lightweight HTTP server running inside the consumer process, exposing the current metrics for Prometheus to scrape.

---

## Prometheus Verification

Verified:

* Kafka Broker running
* Consumer running
* FastAPI running
* Prometheus Server running
* Status → Targets = **UP**

Executed query:

```promql
processed_events_total
```

Initial value:

```text
0
```

After publishing events:

```text
processed_events_total = 5
```

---

## Counter vs Gauge

**Counter**

* Only increases (except application restart)
* Example:

  * processed_events_total
  * retry_events_total
  * dlq_events_total

**Gauge**

* Can increase or decrease
* Example:

  * consumer_lag

---

## First PromQL Function

Learnt:

```promql
rate(processed_events_total[1m])
```

Understanding:

* Calculates the average per-second increase of a counter over the selected time window.
* Uses multiple scraped samples instead of just the latest value.
* Internally estimates the trend using linear regression while handling counter resets and irregular scrape timings.

Practical verification:

* Published multiple events over approximately one minute.
* Observed a non-zero rate value.

---

## Important Concept

Prometheus stores **samples**, not every event.

Grafana visualizes only the data that Prometheus has collected.

Missing samples cannot be recreated later.

---

## Pending Tasks

* Recreate `signup-dlq-events`
* Investigate recurring KRaft metadata issue (instead of deleting `kraft-combined-logs`)
* Learn:

  * `increase()`
  * `sum()`
  * `avg()`
  * `max()`
  * Labels
* Connect Grafana with Prometheus
* Build first dashboard
