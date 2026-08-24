import uuid
from datetime import datetime, timezone
from app.models.schemas import EventEnvelope, OrderRequest
from app.kafka_client.producer import publish_events
from app.repositories.order_repository import get_orders_by_user, get_order_by_id

def create_order_event(order: OrderRequest, user_id: int):
    event = EventEnvelope(
        event_id=str(uuid.uuid4()),
        event_type="ORDER_CREATED",
        event_version=1,
        timestamp=datetime.now(timezone.utc),
        source="fastapi",
        payload={**order.model_dump(),"user_id": user_id}
    )
    publish_events(event.model_dump(mode="json"))
    return event

def get_orders(user_id: int):
    orders = get_orders_by_user(user_id)
    return [
        {
            "order_id": order[0],
            "customer_name": order[1],
            "amount": float(order[2]),
            "event_id": order[3]
        }
        for order in orders
    ]
    
def get_user_order(order_id: str, user_id: int):
    order = get_order_by_id(order_id, user_id)
    if not order:
        return None
    return {
        "order_id": order[0],
        "customer_name": order[1],
        "amount": float(order[2]),
        "event_id": order[3]
    }