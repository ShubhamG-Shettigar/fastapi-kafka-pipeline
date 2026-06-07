from prometheus_client import Counter, Gauge

processed_events_total = Counter(
    "processed_events_total",
    "Total successfully processed Kafka events"
)

retry_events_total = Counter(
    "retry_events_total",
    "Total Kafka event retries"
)

dlq_events_total = Counter(
    "dlq_events_total",
    "Total Kafka events moved to DLQ"
)

consumer_lag = Gauge(
    "consumer_lag",
    "Current Kafka consumer lag"
)