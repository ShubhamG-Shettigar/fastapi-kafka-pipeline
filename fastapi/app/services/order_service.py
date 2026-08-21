import uuid
from datetime import datetime, timezone
from app.models.schemas import EventEnvelope, OrderRequest
from app.kafka_client.producer import publish_events

def create_order_event(order: OrderRequest):
    event = EventEnvelope(
        event_id=str(uuid.uuid4()),
        event_type="ORDER_CREATED",
        event_version=1,
        timestamp=datetime.now(timezone.utc),
        source="fastapi",
        payload=order.model_dump()
    )
    publish_events(event.model_dump(mode="json"))
    return event