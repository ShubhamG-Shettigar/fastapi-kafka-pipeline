# Day 32 – Backend Switch (Warm Restart)

## Objective

Resume the Backend Switch project after a ~20-day break by rebuilding the Prometheus mental model and verifying the existing setup.

---

## Project Status Verified

Successfully started:

* Kafka Broker
* Kafka Consumer
* FastAPI Server

Verified metrics endpoint:

```text
http://localhost:8001
```

Custom metrics were visible:

* processed_events_total
* retry_events_total
* dlq_events_total
* consumer_lag

---

## Prometheus Revision

### Prometheus Client vs Prometheus Server

**Prometheus Client (Python Library)**

* Runs inside the consumer application.
* Exposes the `/metrics` endpoint.
* Metrics are stored only in the application's RAM.

**Prometheus Server**

* Runs as a separate application.
* Periodically scrapes the `/metrics` endpoint.
* Stores metrics as time-series data with timestamps.

---

## Configuration File

Project configuration:

```text
fastapi/prometheus.yml
```

Current configuration:

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: consumer_metrics

    static_configs:
      - targets: ['localhost:8001']
```

Key understanding:

* Prometheus can use **any** configuration file specified through `--config.file`.
* The configuration file inside the Prometheus installation is not a parent configuration; it is simply another configuration file.

---

## Command Used

From the Prometheus installation folder:

```bash
prometheus.exe --config.file=<path-to-project>\fastapi\prometheus.yml
```

---

## Verification Steps

Opened:

```text
http://localhost:9090
```

Verified:

Status → Targets

Result:

```text
consumer_metrics → UP
```

Successfully queried:

* processed_events_total
* retry_events_total
* consumer_lag

---

## Important Learning

Two independent refresh cycles exist:

1. **Prometheus Scraping**

* Controlled by `scrape_interval`.
* Automatically fetches metrics from the application.

2. **Prometheus UI**

* Does not auto-refresh query results.
* Browser refresh or query re-execution is required to view newly scraped values.

---

## Interview Takeaway

The `/metrics` endpoint only exposes the application's current in-memory metrics.

Historical metrics are stored by **Prometheus**, while **Grafana only visualizes** the data stored in Prometheus.

---

## Tomorrow's Plan

1. Investigate recurring KRaft metadata issue.
2. Recreate missing `signup-dlq-events` topic.
3. Refresh PromQL basics.
4. Begin Grafana setup and connect it to Prometheus.
