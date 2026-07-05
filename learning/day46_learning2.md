# Day 46 (Evening) - Learning Log

## Topics Covered

### 1. Grafana Connected to Prometheus

Successfully added Prometheus as a Grafana Data Source.

Configuration:

```text
URL:
http://localhost:9090
```

Verified using **Save & Test**.

Result:

* Successfully queried the Prometheus API.
* Grafana can now execute PromQL queries through Prometheus.

---

### 2. Understanding Grafana's Role

Revised architecture:

```text
Consumer
      │
      ▼
Prometheus (/metrics scraping)
      │
Stores Time Series
      ▼
Prometheus API + PromQL Engine
      ▲
      │
Grafana (Visualization Layer)
```

Key Learning:

* Prometheus executes PromQL.
* Grafana does **not** understand PromQL.
* Grafana sends PromQL queries to Prometheus and visualizes the returned results.

---

### 3. First Dashboard

Created the first Grafana Dashboard using **Auto Grid**.

Created the first visualization panel.

Executed the first PromQL query:

```promql
processed_events_total
```

Successfully visualized the application's metric as a live graph.

---

### 4. Multiple Metrics on One Panel

Added multiple PromQL queries to the same panel.

Queries used:

```promql
processed_events_total
retry_events_total
dlq_events_total
```

Observation:

* Grafana automatically plotted multiple time series with different colors.
* Learned that one panel can visualize multiple related metrics together.

---

### 5. Live Experiment

Performed live testing by pushing additional events.

Observed:

* Counter values increased.
* Prometheus scraped updated values.
* Grafana refreshed and displayed new points on the graph.

This completed the full observability flow from application → dashboard.

---

### 6. Consumer Crash Experiment

Accidentally introduced a bug (`conn.rollback()` typo), causing the consumer to crash.

Observed Grafana behaviour:

* Metrics remained flat while the consumer was down.
* After restart, processing resumed.
* Retry counter increased.
* DLQ counter increased after retry.

Important Learning:

The visible delay was caused primarily by Prometheus waiting for the next scrape interval before discovering updated metric values.

---

### 7. Thinking Beyond Existing Metrics

Discussed metrics that would be valuable in production.

Current metrics:

* processed_events_total
* retry_events_total
* dlq_events_total

Potential future metrics:

* consumer_lag (Gauge)
* active_messages (Gauge)
* processing_duration_seconds (Histogram)
* db_insert_duration_seconds (Histogram)

This marked the transition from **using monitoring** to **designing monitoring**.

---

## Commands / Queries Used

```promql
processed_events_total
```

```promql
retry_events_total
```

```promql
dlq_events_total
```

---

## Key Takeaways

* Grafana is only a visualization layer.
* Prometheus is responsible for executing PromQL.
* Multiple metrics can be plotted on the same panel.
* Dashboards tell the story of the application, not just individual metric values.
* Experiments and failures (consumer crash, retries, DLQ) make Grafana much more meaningful than static graphs.

---

## Progress

Completed:

* Grafana Installation ✅
* Prometheus Data Source ✅
* First Dashboard ✅
* First Panel ✅
* Live Metrics Visualization ✅
* Multi-Series Graphs ✅

---

## Next Session

* Explore different visualization types (Stat, Gauge, Time Series).
* Understand labels from Grafana's perspective.
* Aggregation operators.
* `sum()`, `avg()`, `max()`.
* `by()` and `without()`.
* Begin building a production-style dashboard layout.
