import uuid
from datetime import datetime, timezone
from fastapi import APIRouter
from app.models.schemas import OrderRequest, EventEnvelope
from app.kafka_client.producer import publish_events

router = APIRouter()

@router.post("/orders")
def create_order(order: OrderRequest):
    event = EventEnvelope(
        event_id=str(uuid.uuid4()),
        event_type="ORDER_CREATED",
        event_version=1,
        timestamp=datetime.now(timezone.utc),
        source="fastapi",
        payload=order.model_dump()
    )
    publish_events(event.model_dump(mode="json"))
    return {
        "message": "Order event published",
        "event_id": event.event_id
    }