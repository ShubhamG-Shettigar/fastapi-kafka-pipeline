# Backend Switch — Day 54

## Today's Work

### 1. GET `/orders/{order_id}`

Implemented specific order retrieval with user-level authorization.

Flow:

```text
JWT → username → user_id
                 ↓
       order_id + user_id
                 ↓
             PostgreSQL
```

Repository query:

```sql
WHERE order_id = %s
AND user_id = %s
```

This ensures a user can only retrieve their own order.

### 2. Service + Route

Added:

```text
get_order_by_id()
get_user_order()
GET /orders/{order_id}
```

`fetchone()` is used because `order_id` is unique and we expect one order or none.

### 3. Testing

All passed:

```text
User A → own order        → 200 ✅
User A → User B's order   → 404 ✅
User A → fake order       → 404 ✅
```

We intentionally return `404` instead of revealing that another user's order exists.

---

## Real-World Connection

Users don't manually remember `order_id`.

Typical flow:

```text
GET /orders
     ↓
Frontend receives order IDs
     ↓
User clicks an order
     ↓
Frontend automatically calls
GET /orders/{order_id}
```

Swagger is only our testing interface.

---

## Key Concept

**Authentication:** Who are you?

```text
JWT → user_id
```

**Authorization:** Are you allowed to access this order?

```text
order_id + user_id → ownership check
```

---

## Current Project Status

We now have:

```text
FastAPI
  ↓
JWT Authentication
  ↓
Kafka Order Events
  ↓
Kafka Consumer
  ↓
PostgreSQL
  ↓
User-specific Order Retrieval
  ↓
Object-level Authorization
```

### Next Session

**Pause feature development and review the overall project roadmap.**

We'll decide what is genuinely worth implementing next and how close we are to the final Backend Switch goal.
