# Day 28 - Prometheus Practical (Part 1)

## 1. Metrics vs Prometheus

Important realization:

Creating:

* Counter
* Gauge
* start_http_server()

DOES NOT mean Prometheus is running.

Current status:

Application
↓
Prometheus Metrics Format
↓
Metrics Endpoint

Prometheus Server
↓
Not installed yet

---

## 2. Metrics Created

File:

app/metrics.py

Metrics:

* processed_events_total (Counter)
* retry_events_total (Counter)
* dlq_events_total (Counter)
* consumer_lag (Gauge)

Reason:

Counter:

* Only increases

Gauge:

* Can increase or decrease

---

## 3. Consumer Integration

Imported metrics into consumer.py

Replaced:

processed_events += 1

with:

processed_events_total.inc()

Replaced:

retry_events += 1

with:

retry_events_total.inc()

Replaced:

dlq_events += 1

with:

dlq_events_total.inc()

Added temporary:

consumer_lag.set(0)

---

## 4. Metrics Endpoint

Added:

from prometheus_client import start_http_server

and:

start_http_server(8001)

before consumer loop.

Result:

http://localhost:8001

shows Prometheus metrics.

---

## 5. Important Discovery

Current metrics are stored in:

Consumer Process Memory

Therefore:

Consumer Restart
↓
Metrics Reset To Zero

Expected behavior.

Reason:

Prometheus Server is not scraping yet.

No historical storage exists yet.

---

## 6. Understanding start_http_server()

This starts:

A tiny HTTP server

Its purpose:

Expose metrics for Prometheus scraping.

It is NOT Prometheus.

Think:

"Metrics Producer"

not

"Metrics Storage"

---

## 7. Prometheus Metrics Format

Observed:

# HELP processed_events_total ...

# TYPE processed_events_total counter

processed_events_total 0.0

Meaning:

HELP:

* Description

TYPE:

* Metric Type

Value:

* Current Snapshot

---

## 8. Concurrency vs Parallelism

Concurrency:

* Multiple tasks making progress during same period.
* Can use:

  * Processes
  * Threads
  * Async/Await

Parallelism:

* Multiple tasks executing simultaneously.

Interview One-Liner:

Concurrency = dealing with multiple tasks at once

Parallelism = executing multiple tasks at once

---

## 9. Current Architecture

Consumer
│
├── Counters
├── Gauge
│
└── Metrics Endpoint (8001)

Prometheus
↓
Not Connected Yet

Grafana
↓
Not Connected Yet

---

## Next Session

Prometheus Server Installation

Consumer
↓
Prometheus Scraping
↓
Time-Series Storage
↓
Grafana Visualization

This is where observability becomes fully functional.
