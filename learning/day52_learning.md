# Learning Notes — JWT Configuration & Authentication Flow

## 1. JWT Configuration Refactor

Earlier, JWT configuration was hardcoded inside `auth_service.py`:

* `SECRET_KEY`
* `ALGORITHM`
* `ACCESS_TOKEN_EXPIRE_MINUTES`

We moved these into `.env` and centralized them through `settings.py`.

Flow:

`.env → settings.py → auth_service.py`

`.env` is excluded from Git using the root `.gitignore`:

```text
fastapi/.env
```

This keeps secrets/configuration outside the application source code.

## 2. auth_service.py

`auth_service.py` is responsible for authentication-related operations:

* `hash_password()` → bcrypt-hashes passwords
* `verify_password()` → compares plain password with stored hash
* `create_access_token()` → generates JWT
* `verify_token()` → decodes and validates JWT

The actual JWT secret is now obtained through:

```python
settings.jwt_secret_key
```

## 3. Authentication Flow

### Signup

```text
Client
  ↓
POST /auth/signup
  ↓
Password is hashed
  ↓
User stored in PostgreSQL
```

The original password is NOT stored in PostgreSQL.

### Login

```text
Client
  ↓
POST /auth/login
  ↓
Password verified against bcrypt hash
  ↓
JWT Access Token generated
  ↓
Token returned to client
```

We tested this successfully with a new user.

## 4. Why Do We Need JWT?

The password is used to authenticate the user during login.

After successful authentication, the server gives the client a temporary JWT.

The client uses that JWT for subsequent protected requests instead of repeatedly sending the password.

```text
Login → prove identity → receive JWT
JWT → carry authenticated identity → access protected APIs
```

Authentication answers:

> Who are you?

Authorization answers:

> Are you allowed to access this resource?

## 5. Current State of Our Project

Currently JWT generation works, but the token is **not yet being used to protect `/orders`**.

So:

```text
Signup
  ↓
Login
  ↓
JWT generated
  ↓
[JWT currently stops here]
```

## 6. Next Session — JWT Protection

Next we will connect `verify_token()` to FastAPI using a reusable authentication dependency.

Target flow:

```text
Login
  ↓
JWT
  ↓
Client stores token
  ↓
POST /orders
Authorization: Bearer <JWT>
  ↓
FastAPI authentication dependency
  ↓
verify_token()
  ↓
Valid?
 ├── No → 401 Unauthorized
 └── Yes
       ↓
   Order Service
       ↓
   EventEnvelope
       ↓
      Kafka
       ↓
    Consumer
       ↓
   PostgreSQL
```

Swagger will also be configured with an **Authorize 🔒** mechanism so the token can be supplied once and automatically attached to protected requests.

## Key Learning

**Signup = Create identity**

**Login = Prove identity + receive token**

**JWT = Authenticated credential**

**Protected Order API = Use that credential to perform business operations**
