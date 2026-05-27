# Day 16 — Dependency Injection & Request Lifecycle

## Completed

* Created `get_db()` dependency function
* Introduced FastAPI `Depends()`
* Converted `/signup` route to use dependency injection
* Implemented automatic cursor cleanup using `yield`

---

## get_db()

```python
def get_db():

    cursor = conn.cursor()

    try:
        yield cursor

    finally:
        cursor.close()
```

---

## Important Concepts

### Dependency Injection (DI)

Framework automatically provides required resources to routes.

Instead of:

```python
cursor = get_cursor()
```

used:

```python
cursor = Depends(get_db)
```

---

### yield

`yield` pauses function instead of ending it.

Flow:

```text
create cursor
↓
yield cursor to route
↓
route executes
↓
function resumes
↓
finally block runs
↓
cursor closes
```

---

### Request Lifecycle

Each request now gets:

* fresh cursor
* automatic cleanup after request

This avoids:

* cursor leaks
* manual cleanup handling
* shared cursor issues

---

## Major Learning

Shift from:

```text
manual resource management
```

toward:

```text
framework-managed request lifecycle
```

FastAPI now automatically:

* creates resources
* injects them
* cleans them up
