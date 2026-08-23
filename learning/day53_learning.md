# Backend Switch — Learning Notes

## Today's Focus

Implemented user ownership for orders and built a user-specific `GET /orders` API.

---

## 1. User → Order Relationship

Added `user_id` to the `orders` table.

```text
auth_users
    id
     ↓
orders.user_id
```

Implemented:

```sql
FOREIGN KEY (user_id)
REFERENCES auth_users(id)
```

Constraint name:

```text
fk_orders_user
```

The constraint name is only a label used to identify/manage the constraint. The FK works without explicitly naming it too.

---

## 2. Referential Integrity Test

Deliberately tried inserting an order with:

```text
user_id = 1111
```

when user `1111` did not exist.

PostgreSQL rejected the insert:

```text
violates foreign key constraint "fk_orders_user"
```

Confirmed that the invalid order was not inserted.

### Key takeaway

PostgreSQL itself enforces referential integrity.

```text
JWT       → Authentication
Kafka     → Event transport
PostgreSQL → Data integrity
```

---

## 3. Repository Layer

Introduced:

```text
app/repositories/
    user_repository.py
    order_repository.py
```

Responsibilities:

```text
Repository → Database queries
Service    → Application/business logic
Route      → HTTP/API handling
```

### User lookup

`get_user_by_username()` uses:

```python
fetchone()
```

because username is unique and we expect at most one matching user.

### Order lookup

`get_orders_by_user()` uses:

```python
fetchall()
```

because one user can have multiple orders.

Important distinction:

```text
fetchone() → returns one row
fetchall() → returns a list of all matching rows
```

Even if `fetchall()` finds only one user, it still returns a list containing one row.

---

## 4. JWT → User ID

The JWT contains the username in:

```text
sub
```

Flow:

```text
JWT
 ↓
username
 ↓
auth_users lookup
 ↓
user_id
```

We do not ask the client to provide `user_id`.

The server derives it from the authenticated user's JWT.

---

## 5. user_id Through Kafka

`order_service.py` was updated so that `user_id` becomes part of the event payload.

```python
payload={
    **order.model_dump(),
    "user_id": user_id
}
```

`**` unpacks the dictionary returned by `model_dump()`.

Example:

```python
{
    **order_data,
    "user_id": 111
}
```

becomes:

```python
{
    "order_id": "order-123",
    "customer_name": "Shubham",
    "amount": 19000,
    "user_id": 111
}
```

Flow:

```text
JWT
 ↓
user_id
 ↓
order_service
 ↓
Kafka event
 ↓
consumer
 ↓
orders.user_id
```

---

## 6. Kafka Offset Observation

Our consumer uses:

```python
auto_offset_reset="earliest"
```

and:

```python
enable_auto_commit=False
```

with manual:

```python
consumer.commit()
```

Observed:

```text
processed message offset = 2
committed offset = 3
```

Important:

> Kafka commits the next offset to consume.

So processing offset `2` successfully results in committing offset `3`.

Also observed that older events without `user_id` failed with:

```text
KeyError: 'user_id'
```

Our existing retry/DLQ mechanism handled those failures.

This demonstrated an important real-world issue:

> Changing an event schema can make older events incompatible with newer consumers.

---

## 7. GET /orders

Implemented:

```text
GET /orders
```

Flow:

```text
GET /orders
     ↓
JWT authentication
     ↓
identify username
     ↓
find user_id
     ↓
SELECT orders WHERE user_id = ?
     ↓
return user's orders
```

Unlike `POST /orders`, GET does not need Kafka.

```text
POST /orders
    ↓
Kafka
    ↓
Consumer
    ↓
PostgreSQL

GET /orders
    ↓
PostgreSQL
    ↓
Response
```

POST is an event/action; GET is a query.

---

## 8. Clean API Response

Initially PostgreSQL tuples were returned directly:

```text
[
    ["order-123", "Shubham", 19000, "..."]
]
```

Created:

```python
class OrderResponse(BaseModel):
    order_id: str
    customer_name: str
    amount: float
    event_id: str
```

The service converts DB tuples into dictionaries, and FastAPI uses:

```python
response_model=list[OrderResponse]
```

Final API response:

```json
[
  {
    "order_id": "order-123",
    "customer_name": "Shubham",
    "amount": 19000,
    "event_id": "..."
  }
]
```

This gives the API a clear response contract instead of exposing raw database tuples.

---

## 9. Multi-User Authorization Test

Created a second user.

### User A

```text
user_id = 111
```

Had 3 orders.

### User B

```text
user_id = 112
```

Had 1 order.

Tested:

```text
User B → GET /orders
```

Result:

```text
Only User B's 1 order
```

Then:

```text
User A → GET /orders
```

Result:

```text
Only User A's 3 orders
```

Finally verified PostgreSQL:

```text
orders
--------------------------------
order 1 → user_id 111
order 2 → user_id 111
order 3 → user_id 111
order 4 → user_id 112
```

### Key takeaway

Authentication answers:

> Who are you?

JWT identifies the user.

Authorization answers:

> What data are you allowed to access?

Our query:

```sql
WHERE user_id = %s
```

ensures users only receive their own orders.

---

# Current Architecture

```text
                    JWT
                     ↓
              Authentication
                     ↓
                user_id
                     ↓
POST /orders → order_service
                     ↓
                   Kafka
                     ↓
                 Consumer
                     ↓
                PostgreSQL
                     ↑
                     │
GET /orders → order_service
                     ↑
               repository
```

Database relationship:

```text
auth_users
    │
    │ id
    │
    │ FK
    ↓
orders.user_id
```

---

# Completed So Far

* FastAPI application
* Signup/Login
* Password hashing
* JWT authentication
* Protected order routes
* Kafka order events
* Kafka consumer
* Retry/DLQ handling
* PostgreSQL persistence
* User/order relationship
* Foreign key + referential integrity
* Repository layer
* User-specific GET /orders
* Pydantic response models
* Multi-user authorization testing

---

# Next Session

## GET `/orders/{order_id}`

Goal:

```text
User A knows User B's order_id
             ↓
     tries GET /orders/{id}
             ↓
          DENIED
```

This will demonstrate **object-level authorization** — not just protecting the route, but ensuring a user cannot access another user's specific order.
