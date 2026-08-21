from fastapi import APIRouter, Depends
from app.models.schemas import OrderRequest
from app.services.order_service import create_order_event
from app.dependencies.auth_dependency import get_current_user

router = APIRouter()
@router.post("/orders")
def create_order(
    order: OrderRequest,
    current_user: dict = Depends(get_current_user)
):
    event = create_order_event(order)
    return {
        "message": "Order event published",
        "event_id": event.event_id
    }