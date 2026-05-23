# Day 13 — JWT Authentication + Protected Routes

## Topics Covered

- Password hashing lifecycle
- Signup vs Login flow
- JWT basics
- Access token generation
- Token verification
- Protected API routes
- Authorization flow understanding
- FastAPI query/header confusion debugging
- Python package/import concepts

---

# 1. Signup vs Login Flow

## Signup

New user registers.

Flow:
- frontend sends username/password
- backend hashes password
- hashed password stored in DB

Important:
- `verify_password()` NOT used here
- because no existing password exists yet

---

## Login

Existing user logs in.

Flow:
- frontend sends username/password
- backend fetches hashed password from DB
- `verify_password()` compares entered password
- if valid:
  - `create_access_token()` called
  - JWT token generated
  - token returned to frontend

---

# 2. JWT Understanding

JWT is:
- digitally signed identity token

JWT contains:
- user identity (`sub`)
- expiry (`exp`)

Example payload:
```json
{
  "sub": "shubham",
  "exp": 1779521987
}