from fastapi import APIRouter
from app.models.schemas import OrderRequest
from app.services.order_service import create_order_event

router = APIRouter()
@router.post("/orders")
def create_order(order: OrderRequest):
    event = create_order_event(order)
    return {
        "message": "Order event published",
        "event_id": event.event_id
    }