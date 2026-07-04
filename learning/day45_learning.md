# Day 45 – Backend Switch

## Duration

~1.5 Hours (Weekend Lite)

---

# Environment Setup

Verified:

* Kafka Broker ✅
* Consumer ✅
* FastAPI (Uvicorn) ✅
* Prometheus Server ✅

---

# Kafka

## Topic Cleanup

Observed duplicate DLQ topic names:

* `signup-events-dlq` ✅ (Used by consumer)
* `signup-dlq-events` ❌ (Accidentally created)

Deleted the incorrect topic.

During deletion, broker encountered another KRaft-related issue, requiring storage recreation.

After recreating the KRaft storage:

Topics present:

* `signup-events`
* `signup-events-dlq`
* `__consumer_offsets`

Current setup is clean.

**Future Task**

Investigate the recurring KRaft issue properly using broker logs instead of recreating storage immediately.

---

# PromQL

## Revision

Learnt difference between:

### `rate()`

Returns the **average per-second increase** of a counter over the selected time window.

Example:

```promql
rate(processed_events_total[1m])
```

---

### `increase()`

Returns the **total increase** of the counter during the selected time window.

Example:

```promql
increase(processed_events_total[1m])
```

Important observation:
increase = rate x time window
`increase()` may return decimal values (e.g. `5.32`) because Prometheus estimates values at the query window boundaries using sampled data instead of performing a simple `last - first` calculation.

---

### `sum()`

Aggregates the same metric across multiple instances.

Example:

```promql
sum(processed_events_total)
```

---

### `avg()`

Returns the average value.

Useful for average consumer lag.

---

### `max()`

Returns the maximum value.

Useful for identifying the worst-performing consumer.

---

# Labels

Verified automatically added labels:

* `job = consumer_metrics`
* `instance = localhost:8001`

Understanding:

* Prometheus automatically adds scrape-related labels.
* Application-specific labels can also be defined inside the Python code while creating metrics.

Labels discussion intentionally postponed for a dedicated session.

---

# Practical Verification

Verified:

* `processed_events_created`

Observation:

Restarting Prometheus does **not** change the timestamp.

Restarting the consumer **does** change the timestamp because the metric object is recreated inside the Python process.

---

# DLQ Verification

Verified successful DLQ event processing.

Observed corresponding DLQ metric increment correctly.

---

# Next Session

* Deep dive into Labels
* PromQL filtering using labels
* `by()` aggregation
* Connect Grafana with Prometheus
* Build first Grafana dashboard
