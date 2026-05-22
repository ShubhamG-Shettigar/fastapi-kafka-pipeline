# Day 12 - Authentication Fundamentals & Password Hashing

## Objective

Started authentication and security fundamentals for backend systems.

Focus today:

* Why authentication is needed
* Session vs JWT understanding
* Password hashing
* Salt concept
* Password verification logic

---

# Why Authentication Exists

Without authentication:
any user can access protected APIs.

Example:
POST /send-money

Without identity verification:
anyone could call this API.

Authentication helps backend identify:
“Who is making the request?”

---

# Traditional Session-Based Authentication

Old websites commonly used:

* sessions
* cookies

Flow:

1. User logs in
2. Server creates session
3. Session stored server-side
4. Browser gets session-id cookie
5. Browser sends cookie in future requests
6. Server validates session

---

# Problem With Sessions in Distributed Systems

In large systems:

* multiple backend servers
* microservices
* auto-scaling

Issue:
Which server stores session?

Need:
centralized session storage like:

* Redis
* DB

Otherwise:
request hitting different server may lose session context.

---

# JWT Advantage

JWT provides:
stateless authentication.

Meaning:
server does not need centralized session storage.

JWT contains:

* user identity
* metadata
* expiry
* digital signature

Any backend server can independently validate JWT.

Useful for:

* APIs
* microservices
* distributed systems

---

# Password Hashing

Never store plain passwords in DB.

Bad:
india123

Instead:
store hashed password.

Example:
$2b$12$....

Hashing is:

* one-way
* non-reversible
* secure transformation

---

# bcrypt

Used bcrypt hashing algorithm via:

* passlib
* bcrypt

bcrypt advantages:

* slow hashing
* brute-force resistant
* industry standard
* built-in salting

---

# auth.py Created

Implemented:

```python
from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def hash_password(password: str):

    return pwd_context.hash(password)
```

---

# Password Verification

Implemented:

```python
def verify_password(plain_password, hashed_password):

    return pwd_context.verify(
        plain_password,
        hashed_password
    )
```

Purpose:
verify entered password against stored hash.

---

# Important Observation

Hashing same password multiple times:
produces DIFFERENT hashes.

Reason:
bcrypt automatically generates random SALT.

---

# Salt Concept

Salt =
random value added before hashing.

Without salt:
same password → same hash.

Problem:
attackers can:

* identify users sharing passwords
* use rainbow tables

---

# Rainbow Table Attack

Attackers precompute:

password → hash mappings

Example:

123456 → HASH_1
password → HASH_2

If DB leaked:
hashes become easier to crack.

---

# Why Salt Helps

With salt:
same password produces different hashes.

Example:

india123 + ABC → HASH_X
india123 + XYZ → HASH_Y

So:

* identical passwords no longer look identical
* rainbow tables become ineffective

---

# Major Confusion Clarified

Question:
If salt changes hash every time,
how does verification work?

Answer:
bcrypt stores original salt INSIDE stored hash.

During verification:

* bcrypt extracts original salt
* hashes entered password using SAME salt
* compares mathematically

Therefore:
same password + same salt
→ same resulting hash.

---

# Important Insight

Fresh hashing:
new random salt generated.

Verification:
stored salt reused.

Therefore:

* new hashes differ
* verification still succeeds correctly

---

# Additional Security Concept

Mentioned:
PEPPER

Pepper =
secret extra server-side value added before hashing.

Unlike salt:
pepper is NOT stored in DB.

Used as additional security layer.

---

# Practical Work Completed

* Installed:

  * passlib
  * bcrypt
  * python-jose

* Fixed bcrypt compatibility issue

* Generated hashed passwords successfully

* Verified:

  * correct password → True
  * wrong password → False

---

# Key Takeaway

Authentication security is not just:
“store password.”

It involves:

* hashing
* salts
* secure verification
* attack resistance
* distributed authentication strategies

Strong backend security foundation started today.
