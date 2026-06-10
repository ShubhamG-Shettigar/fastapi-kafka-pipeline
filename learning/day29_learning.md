# Day 29 - Prometheus Architecture Understanding

## 1. Important Realization

Until now:

Prometheus Server was NOT installed.

We only used:

prometheus_client

inside the application.

This means:

Consumer
↓
Metrics Endpoint

was working,

but

Prometheus
↓
Scraping
↓
Storage

did not exist yet.

---

## 2. Current Architecture

Consumer
│
├── Counters
├── Gauge
│
└── start_http_server(8001)

Result:

localhost:8001

shows metrics successfully.

---

## 3. Why Metrics Reset After Restart

Observation:

Consumer Restart
↓
Metrics Reset To 0

Reason:

Metrics currently live inside:

Process Memory

No Prometheus Server exists yet.

Therefore:

No historical storage exists.

Expected behavior.

---

## 4. Metrics Exposure vs Prometheus

Important distinction:

start_http_server(8001)

DOES NOT start Prometheus.

It only creates:

A small HTTP endpoint

that exposes metrics.

Think:

Metrics Producer

NOT

Metrics Storage.

---

## 5. Port Understanding

8001

Purpose:

Consumer Metrics Endpoint

Chosen for convenience.

No special meaning.

Could have been:

5555
7777
9999

etc.

---

9090

Default Prometheus Port.

Industry convention.

Not mandatory.

Prometheus can run on another port if configured.

---

## 6. Understanding Port Responsibility

Port Number
≠
Functionality

# Process Running On Port

Functionality

Example:

8001 is not metrics.

# Metrics Endpoint running on 8001

Metrics.

---

## 7. prometheus.yml

Created:

fastapi/prometheus.yml

Purpose:

Configuration file for Prometheus.

YAML is:

Configuration

NOT

Application Logic.

Current content:

global:
scrape_interval: 15s

scrape_configs:

* job_name: 'consumer_metrics'

  static_configs:

  * targets: ['localhost:8001']

Meaning:

Every 15 seconds:

Prometheus should fetch metrics from:

localhost:8001

---

## 8. Next Session Starting Point

Download Prometheus

↓

Run prometheus.exe

↓

Use prometheus.yml

↓

Open localhost:9090

↓

Verify Target Status

↓

Query Metrics

↓

Observe Historical Data

---

## Key Takeaway

Metrics Endpoint
≠
Prometheus

Prometheus Client
≠
Prometheus Server

Today clarified the architecture before installing the actual Prometheus server.
