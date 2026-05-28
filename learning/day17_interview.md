# interview.md — Day 17

## Tricky Question

### Question

Suppose this route exists:

```python
@router.get("/data")
async def get_data():

    result = cursor.execute("SELECT * FROM users")

    return result
```

Interviewer asks:

```text
“Since route is async,
does this automatically make DB query non-blocking?”
```

---

## Correct Answer

NO.

Reason:

* `async def` only makes route coroutine-capable
* `psycopg2` is still synchronous/blocking
* DB query still blocks execution internally
* true async requires async-compatible DB driver

Examples:

* asyncpg
* SQLAlchemy async engine

---

## Key Insight

Async has TWO layers:

### 1. Async route

```python
async def
```

### 2. Async internal operations

```python
await async_db_call()
```

Without layer 2:

```text
benefit is partial
```

---

## Interview Keywords

* event loop
* cooperative multitasking
* non-blocking IO
* synchronous DB driver
* concurrency
* async ecosystem
