# Learning Notes — JWT Authentication & Protected Orders

## What We Built Today

### 1. Environment-based JWT Secret

Moved the JWT secret out of source code and into `.env`.

```text
.env
  ↓
settings.py
  ↓
auth_service.py
```

The JWT secret is **not the user's password**.

It acts like the backend's cryptographic signing seal used to sign and verify JWTs.

`.env` is excluded from Git using `.gitignore`.

---

## 2. Signup → Login → JWT

### Signup

```text
User password
    ↓
bcrypt hashing
    ↓
PostgreSQL
```

The original password is never stored.

### Login

```text
Username + password
       ↓
Verify against bcrypt hash
       ↓
Valid
       ↓
Generate JWT
       ↓
Return access token
```

The JWT contains claims such as:

```json
{
  "sub": "testjwt",
  "exp": "expiry timestamp"
}
```

The JWT currently expires after **30 minutes**.

The JWT secret itself does **not** expire after 30 minutes.

---

## 3. Stateless JWT Authentication

JWT authentication is stateless because the server does not maintain a login session for every user.

Instead:

```text
Client sends JWT
      ↓
Backend verifies JWT
      ↓
Allow / reject request
```

The server does not need to maintain:

```text
session_id → user
```

for every logged-in client.

---

## 4. JWT Protection for `/orders`

Created:

```text
app/dependencies/auth_dependency.py
```

Implemented:

```python
HTTPBearer()
```

and:

```python
Depends(security)
```

This allows FastAPI to understand:

```text
Authorization: Bearer <JWT>
```

and Swagger automatically provides the:

```text
🔒 Authorize
```

button.

---

## 5. What Swagger Authorize Actually Does

The JWT still has to be supplied.

Swagger is simply acting like a client application.

```text
Login
 ↓
Receive JWT
 ↓
Swagger Authorize
 ↓
Paste JWT once
 ↓
Swagger automatically attaches:
Authorization: Bearer <JWT>
```

We did NOT eliminate the JWT.

We eliminated manually adding/parsing the Authorization header for every request.

---

## 6. Protected Order Flow

Current flow:

```text
POST /orders
      ↓
get_current_user()
      ↓
HTTPBearer extracts JWT
      ↓
verify_token()
      ↓
Valid?
 ├── No → 401 Unauthorized
 └── Yes
       ↓
order_service.py
       ↓
EventEnvelope
       ↓
Kafka
       ↓
Consumer
       ↓
PostgreSQL
```

We successfully tested:

* `/orders` without JWT → `401 Missing authorization header` ✅
* Swagger Authorize with JWT → request accepted ✅
* Multiple orders using the same JWT → successful ✅

Every request independently validates the JWT.

Swagger remaining "unlocked" does NOT mean the backend session remains open.

Once the JWT expires after 30 minutes:

```text
Next request
    ↓
JWT validation
    ↓
Expired
    ↓
401 Unauthorized
```

---

## 7. Refresh Token — Conceptual Understanding

Current system:

```text
Login
 ↓
Access Token (30 min)
 ↓
Expires
 ↓
Login again
```

A refresh-token system would instead provide:

```text
Login
 ↓
Access Token + Refresh Token
 ↓
Access Token expires
 ↓
Use Refresh Token
 ↓
Receive new Access Token
```

We are NOT implementing refresh tokens yet.

---

## 8. Important Architecture Decision

We discussed `GET /orders/{order_id}`.

A user normally won't remember an order ID.

A better real-world flow is:

```text
JWT identifies user
       ↓
POST /orders
       ↓
Order associated with user
       ↓
GET /orders
       ↓
Return that user's orders
```

Currently our `orders` table does **not** associate orders with users.

Therefore we decided **not to rush into the GET endpoint**.

---

# Next Session

### User → Order Ownership

We will implement:

```text
JWT
 ↓
Authenticated user
 ↓
Create order
 ↓
Store user ownership
 ↓
GET /orders
 ↓
Return only that user's orders
```

This will involve:

* Adding user reference to orders
* Passing authenticated user identity to the service
* Storing ownership in PostgreSQL
* Implementing `GET /orders`
* Testing with multiple users to verify isolation

**Current checkpoint:**

```text
Authentication       ✅
JWT generation       ✅
JWT validation       ✅
Protected /orders    ✅
Kafka flow           ✅
PostgreSQL           ✅
Retry / DLQ          ✅

User → Order         ⏭️ Next
GET /orders          ⏭️ Next
```
