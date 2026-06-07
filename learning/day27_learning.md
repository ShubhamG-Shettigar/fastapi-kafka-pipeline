Day 27 - Observability Foundations

1. ELK

* Elasticsearch stores logs.
* Kibana visualizes logs.
* Logstash collects/transforms logs.
* "Check ELK" in many organizations usually means "Check Kibana".

2. Prometheus

* Pull-based metrics collection system.
* Periodically scrapes targets through /metrics endpoint.
* Stores time-series data.
* Stores snapshots, not every intermediate value.

3. Grafana

* Queries Prometheus.
* Does not talk directly to applications.
* Used for dashboards and visualization.

4. Metrics Types

* Counter: Only increases.
  Examples:

  * processed_events_total
  * retry_events_total
  * dlq_events_total

* Gauge: Can increase or decrease.
  Examples:

  * consumer_lag
  * active_connections

5. Logs vs Metrics vs Traces

* Logs = detailed event records.
* Metrics = aggregated numerical measurements.
* Traces = end-to-end request flow tracking using trace IDs.

6. Prometheus Best Practice

* Applications expose raw counters/gauges.
* Prometheus calculates:

  * rate()
  * increase()
  * averages
  * trends

7. Consumer Metrics Added
   Created:

* processed_events_total
* retry_events_total
* dlq_events_total
* consumer_lag

Integrated counters into consumer.py.

8. Important Python Module Note
   Run project from FastAPI root:

uvicorn app.main:app --reload

Use imports:

from app.<module> import ...

to avoid ModuleNotFoundError issues.
