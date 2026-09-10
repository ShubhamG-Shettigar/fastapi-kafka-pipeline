import pytest
from app.services.order_service import is_valid_transition, create_order_event, create_order_status_event
from unittest.mock import patch
from app.models.schemas import OrderRequest
from fastapi.testclient import TestClient
from app.main import app
from app.dependencies.auth_dependency import get_current_user

client = TestClient(app)

def test_unknown_route():
    response = client.get("/does-not-exist")
    assert response.status_code == 404

def test_get_orders_without_auth():
    response = client.get("/orders")
    assert response.status_code == 401
    
def test_get_orders_authenticated():
    app.dependency_overrides[get_current_user] = lambda: {
        "sub": "testuser"
    }
    response = client.get("/orders")
    app.dependency_overrides.clear()
    assert response.status_code == 200
    
    
@pytest.mark.parametrize(
    "current_status,new_status,expected",
    [
        ("CREATED", "CONFIRMED", True),
        ("CONFIRMED", "SHIPPED", True),
        ("SHIPPED", "DELIVERED", True),
        ("CREATED", "CANCELLED", True),
        ("CONFIRMED", "CANCELLED", True),
        ("CREATED", "SHIPPED", False),
        ("DELIVERED", "CANCELLED", False),
        ("DELIVERED", "CONFIRMED", False),
    ]
)
def test_order_status_transition(current_status, new_status, expected):
    result = is_valid_transition(current_status, new_status)

    assert result is expected
    
    
@patch("app.services.order_service.publish_events")
def test_create_order_event(mock_publish):
    order = OrderRequest(
        order_id="test-order-1",
        customer_name="Test User",
        amount=500
    )

    event = create_order_event(order, 1)

    assert event.event_type == "ORDER_CREATED"
    assert event.payload["order_id"] == "test-order-1"
    assert event.payload["user_id"] == 1

    mock_publish.assert_called_once()
    
    
@patch("app.services.order_service.publish_events")
def test_create_order_status_event(mock_publish):
    event = create_order_status_event("order-123", "SHIPPED")

    assert event.event_type == "ORDER_SHIPPED"
    assert event.payload["order_id"] == "order-123"
    assert event.payload["status"] == "SHIPPED"

    mock_publish.assert_called_once()