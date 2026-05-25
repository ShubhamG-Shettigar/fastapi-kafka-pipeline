# Day 14 — JWT Authentication Flow

## Completed

* Created `auth_users` table in PostgreSQL
* Built `/signup` API
* Stored hashed passwords in DB
* Built `/login` API
* Verified passwords using stored hash
* Generated JWT access token after successful login
* Tested:

  * valid login
  * invalid username
  * invalid password

---

## Core Flow Learned

```text
/signup
↓
hash password
↓
store in DB

/login
↓
verify password
↓
generate JWT
↓
return token

future requests
↓
send JWT
↓
verify JWT
↓
access protected APIs
```

---

## Important Concepts

### Password Verification

* Original password is never stored
* Entered password is rehashed using stored salt
* Hashes are compared internally

### JWT

* Acts as temporary proof of authentication
* Password is used only during login
* Future APIs use JWT verification

### fetchone()

* `execute()` only runs query
* `fetchone()` extracts row from cursor result

### Tuple Syntax

```python
(user.username,)
```

* single-element tuple
* required by psycopg2 parameterization

### SQL Injection Prevention

```python
WHERE username=%s
```

with parameter tuple prevents SQL injection.

### Python Imports

Importing a file executes entire file top-to-bottom.

### PostgreSQL Transaction Failure

Failed query can abort transaction state.
Temporary fix:

* restart uvicorn

Production approach:

```python
conn.rollback()
```

---

## Refresh Token Theory

### Access Token

* short-lived
* used for APIs

### Refresh Token

* long-lived
* generates new access tokens
* avoids repeated password login

---

## Major Learning

Authentication flow finally became understandable as:

```text
password
↓
identity verification
↓
JWT issuance
↓
future authenticated communication
```
