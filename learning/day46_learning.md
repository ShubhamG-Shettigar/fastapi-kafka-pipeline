# Day 46 - Learning Log

**Date:** Sunday

## Topics Covered

### 1. Prometheus Labels (Deep Dive)

* Revised automatic labels added by Prometheus:

  * `job`
  * `instance`
* Understood that labels uniquely identify metrics even if metric names are identical.
* Differentiated:

  * **Infrastructure Labels** (instance, pod, namespace, node, job)
  * **Application Labels** (service, tenant, event_type, environment, etc.)
* Learned that application labels are created in the code, whereas infrastructure labels are generally added automatically by Prometheus/Kubernetes.

---

### 2. Multiple Consumer Instances

Discussed how the same consumer code can run multiple instances without modification.

Current project:

```
consumer.py
        │
        ▼
Consumer Instance
```

Production:

```
consumer.py
      │
      ├── Consumer-1
      ├── Consumer-2
      └── Consumer-3
```

Each instance is identified by a unique endpoint (IP:Port or Pod IP), allowing Prometheus to scrape them independently.

---

### 3. Kubernetes Service Discovery

Learned why static targets are only suitable for local development.

Production uses **Service Discovery**, where Prometheus periodically asks Kubernetes for the current list of scrape targets.

Key understanding:

* Service Discovery is a separate loop.
* Metric Scraping is another independent loop.
* Both are pull-based.

---

### 4. Why Discovery Isn't Implemented as Metrics

Discussed architectural reasoning:

* Metrics represent measurements.
* Target discovery represents infrastructure state/configuration.
* Keeping discovery separate from scraping keeps Prometheus modular and allows multiple discovery backends (Kubernetes, EC2, Docker, Consul, etc.).

---

### 5. Grafana Installation

Downloaded and installed Grafana OSS.

Security verification performed before installation:

* Verified official download source.
* Verified SHA256 checksum using PowerShell.

Command used:

```powershell
Get-FileHash .\grafana_13.1.0_28013217238_windows_amd64.msi -Algorithm SHA256
```

Hash matched the official Grafana release.

Installed successfully.

---

### 6. Grafana Service

Verified:

* Grafana installed as a Windows Service.
* Service starts automatically with Windows.
* Accessible at:

```
http://localhost:3000
```

Initial login completed and credentials changed successfully.

---

## Current Observability Stack

```
FastAPI (8000)
        │
        ▼
Kafka Consumer
        │
        ▼
Prometheus Client (/metrics :8001)
        │
        ▼
Prometheus Server (9090)
        │
        ▼
Grafana (3000)
```

---

## Commands Used

### Verify Installer Hash

```powershell
Get-FileHash .\grafana_13.1.0_28013217238_windows_amd64.msi -Algorithm SHA256
```

### Verify Digital Signature (for learning)

```powershell
Get-AuthenticodeSignature .\grafana_13.1.0_28013217238_windows_amd64.msi
```

---

## Progress

* Prometheus Server ✅
* PromQL Basics ✅
* Labels Theory ✅
* Grafana Installation ✅

---

## Next Session

* Connect Grafana to Prometheus.
* Add Prometheus as a Data Source.
* Create the first dashboard.
* Create the first panel using `processed_events_total`.
* Push events and observe live visualization.
* Learn dashboard refresh intervals.
* Begin aggregation with `by()` in a meaningful context.
