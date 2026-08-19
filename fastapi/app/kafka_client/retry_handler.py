from app.kafka_client.producer import publish_events
from app.configs.settings import settings
from app.metrics import retry_events_total, dlq_events_total

MAX_RETRIES = 1
def handle_failure(data):
    retry_count = data.get("retry_count", 0)
    if retry_count < MAX_RETRIES:
        data["retry_count"] = retry_count + 1
        print(
            f"Retrying event... Attempt = {data['retry_count']}"
        )
        publish_events(data, settings.kafka_retry_topic)
        retry_events_total.inc()
        return "moved to retry topic"
    print("Retry limit exhausted. Moving event to DLQ")
    publish_events(data, settings.kafka_dlq_topic)
    dlq_events_total.inc()
    return "moved to dlq topic"