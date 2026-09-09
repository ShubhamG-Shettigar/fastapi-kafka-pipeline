from fastapi import APIRouter, Depends, HTTPException
from app.models.schemas import OrderRequest, OrderResponse
from app.services.order_service import create_order_event, get_orders, get_user_order, change_order_status
from app.dependencies.auth_dependency import get_current_user
from app.services.auth_service import get_user

router = APIRouter()



def update_order_status(
    order_id: str,
    current_user: dict,
    new_status: str
):
    username = current_user["sub"]
    user = get_user(username)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )
    user_id = user[0]
    event = change_order_status(
        order_id,
        user_id,
        new_status
    )
    if event is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )
    if event is False:
        raise HTTPException(
            status_code=400,
            detail="Invalid status transition"
        )
    return {
        "message": f"Order status changed to {new_status}",
        "event_id": event.event_id
    }
    
    
@router.post("/orders")
def create_order(
    order: OrderRequest,
    current_user: dict = Depends(get_current_user)
):
    username = current_user["sub"]
    user = get_user(username)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )
    user_id = user[0]
    event = create_order_event(order, user_id)
    return {
        "message": "Order event published",
        "event_id": event.event_id
    }
   

@router.post("/orders/{order_id}/confirm")
def confirm_order(
    order_id: str,
    current_user: dict = Depends(get_current_user)
):
    return update_order_status(
        order_id,
        current_user,
        "CONFIRMED"
    )

@router.post("/orders/{order_id}/ship")
def ship_order(
    order_id: str,
    current_user: dict = Depends(get_current_user)
):
    return update_order_status(
        order_id,
        current_user,
        "SHIPPED"
    )
    
@router.post("/orders/{order_id}/deliver")
def deliver_order(
    order_id: str,
    current_user: dict = Depends(get_current_user)
):
    return update_order_status(
        order_id,
        current_user,
        "DELIVERED"
    )

@router.post("/orders/{order_id}/cancel")
def cancel_order(
    order_id: str,
    current_user: dict = Depends(get_current_user)
):
    return update_order_status(
        order_id,
        current_user,
        "CANCELLED"
    )
    
@router.get("/orders", response_model=list[OrderResponse])
def get_orders(current_user: dict = Depends(get_current_user)):
    username = current_user["sub"]
    user = get_user(username)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )
    user_id = user[0]
    orders = get_orders(user_id)
    return orders
    
    
@router.get("/orders/{order_id}", response_model=OrderResponse)
def get_order(order_id: str,current_user: dict = Depends(get_current_user)):
    username = current_user["sub"]
    user = get_user(username)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )
    user_id = user[0]
    order = get_user_order(order_id, user_id)
    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )
    return order