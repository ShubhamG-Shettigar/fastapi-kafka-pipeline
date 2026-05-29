# Day 18 — Middleware & Request Lifecycle

## Completed

* Learned middleware basics
* Understood middleware vs normal functions
* Understood middleware vs dependency injection
* Learned request lifecycle
* Added basic middleware in FastAPI

---

# Middleware

## Definition

Middleware is automatic code that executes before and/or after every HTTP request.

---

# Middleware Flow

```text id="mwf1"
Request
↓
Middleware
↓
Route
↓
Middleware
↓
Response
```

---

# Important Property

Middleware runs:

```text id="mwf2"
automatically for requests
```

No manual function call needed.

FastAPI internally executes registered middleware.

---

# Middleware vs Function

## Normal Function

Runs only when explicitly called.

Example:

```python id="mwf3"
greet()
```

---

## Middleware

Runs automatically for request lifecycle.

---

# Middleware vs Dependency

## Middleware

* global request-level logic
* runs for all requests

Examples:

* logging
* auth
* timing
* rate limiting

---

## Dependency Injection

* route-specific resource injection
* executes only when route asks for it

Example:

```python id="mwf4"
Depends(get_db)
```

---

# Important Understanding

`get_db()` from:

```text id="mwf5"
postgres.py
```

is:

```text id="mwf6"
NOT middleware
```

It is a dependency provider.

---

# Middleware Example

```python id="mwf7"
@app.middleware("http")
async def test(request, call_next):

    print("Before route")

    response = await call_next(request)

    print("After route")

    return response
```

---

# Important Line

```python id="mwf8"
await call_next(request)
```

Meaning:

```text id="mwf9"
continue normal request processing
```

---

# Request Lifecycle

```text id="mwf10"
Request arrives
↓
Middleware executes
↓
Route matching
↓
Dependencies execute
↓
Route executes
↓
Response generated
↓
Middleware resumes
↓
Response sent
```

---

# Major Learning

Frameworks like FastAPI are:

```text id="mwf11"
request orchestration engines
```

They automatically manage:

* middleware
* dependencies
* routing
* validation
* responses

---

# Important Mental Shift

Earlier:

```text id="mwf12"
backend looked magical
```

Now:

```text id="mwf13"
request lifecycle is becoming traceable
```
