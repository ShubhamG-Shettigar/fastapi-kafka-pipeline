# Backend Switch — Day 57 Testing Checkpoint

## Today's Goal

Started automated testing for the FastAPI backend.

Focus:

* Unit testing
* Mocking Kafka
* FastAPI API testing
* Authentication behaviour

---

## Testing Setup

Created:

```text
tests/
└── test_basic.py
```

Installed:

```bash
pip install pytest
pip install httpx
```

Run tests using:

```bash
python -m pytest
```

### Why `python -m pytest`?

Running `pytest` directly caused:

```text
ModuleNotFoundError: No module named 'app'
```

But:

```bash
python -m pytest
```

works correctly because it uses the current Python interpreter/environment.

---

# Tests Completed

## 1. Basic Pytest Test

Initially verified that pytest discovers and executes tests.

Also deliberately changed the assertion to make it fail and confirmed that pytest correctly reports failures.

---

## 2. Order Status Transition Tests

Tested `is_valid_transition()` using `pytest.mark.parametrize`.

Covered:

```text
CREATED → CONFIRMED       ✅
CONFIRMED → SHIPPED       ✅
SHIPPED → DELIVERED       ✅
CREATED → CANCELLED       ✅
CONFIRMED → CANCELLED     ✅

CREATED → SHIPPED         ❌
DELIVERED → CANCELLED     ❌
DELIVERED → CONFIRMED     ❌
```

Result:

```text
8 passed
```

---

# 3. Mock Test — Order Creation Event

Tested:

```python
create_order_event()
```

Kafka was mocked using:

```python
@patch("app.services.order_service.publish_events")
```

Verified:

* Event type is `ORDER_CREATED`
* Correct `order_id`
* Correct `user_id`
* Kafka publish function was called exactly once

Important concept:

`create_order_event()` itself runs normally.

Only `publish_events()` is temporarily replaced by a mock.

Therefore:

```text
create_order_event()
       ↓
EventEnvelope created normally
       ↓
mock publish_events()
       ↓
No real Kafka interaction
```

Result:

```text
9 passed
```

---

# 4. Mock Test — Order Status Event

Tested:

```python
create_order_status_event("order-123", "SHIPPED")
```

Verified:

* Event type = `ORDER_SHIPPED`
* Correct order ID
* Correct status
* Kafka publish function called once

Result:

```text
10 passed
```

---

# 5. FastAPI TestClient — Unknown Route

Added FastAPI `TestClient`.

Test:

```python
response = client.get("/does-not-exist")
assert response.status_code == 404
```

This verifies that the FastAPI application correctly handles an unknown endpoint.

Result:

```text
11 passed
```

---

# 6. FastAPI Authentication Test

Tested:

```text
GET /orders
```

without an Authorization header.

Initially expected:

```text
403
```

But the actual application returned:

```text
401 Unauthorized
```

We investigated instead of changing the application unnecessarily.

Our `auth_dependency.py` explicitly raises `401` for authentication failure.

Therefore the test expectation was corrected to:

```python
assert response.status_code == 401
```

Final result:

```text
12 passed
```

---

# Current Test Result

```text
12 passed
2 warnings
```

Warnings:

1. External `pywintypes` deprecation warning
2. Pydantic class-based `Config` deprecation warning

These are intentionally being ignored for now.

---

# Important Testing Concepts Learned

## Unit Test

Tests one piece of application logic in isolation.

Example:

```text
is_valid_transition()
```

---

## Mock

Temporarily replaces an external dependency.

Example:

```text
Kafka publish
```

We can test our application logic without requiring Kafka to actually receive the event.

---

## TestClient

Allows us to test FastAPI endpoints without manually starting Uvicorn.

Conceptually:

```text
Test
 ↓
TestClient
 ↓
FastAPI application
 ↓
Route
 ↓
Dependency / Service
```

---

# Current Testing Progress

```text
Unit Logic
    ↓
    ✅

Kafka Mocking
    ↓
    ✅

FastAPI basic API
    ↓
    ✅

Authentication failure
    ↓
    ✅

Authenticated API
    ↓
    ⏳ NEXT
```

---

# Next Session

## Next Task

Test a successful authenticated:

```text
GET /orders
```

We will NOT use a real JWT or depend unnecessarily on the real database.

Instead, we will learn how to mock/override:

```text
get_current_user
        +
get_user()
```

so the test can focus on the API behaviour.

Expected flow:

```text
TestClient
    ↓
GET /orders
    ↓
Fake authenticated user
    ↓
Fake user lookup
    ↓
Order service
    ↓
API response
```

### Next checkpoint

**Authenticated `/orders` API test using dependency override + mocking.**

---

## End of Day Status

```text
Day 57
Testing phase started successfully

Tests: 12/12 passing
Kafka mocking: DONE
API testing: IN PROGRESS
Authentication testing: IN PROGRESS

Next:
Authenticated GET /orders test
```

