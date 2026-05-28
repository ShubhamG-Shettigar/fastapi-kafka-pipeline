# Day 17 — Async Programming Foundations

## Completed

* Learned async mental model
* Understood blocking vs non-blocking
* Learned event loop basics
* Learned `async def`
* Learned `await`
* Tested async concurrency practically in FastAPI
* Created async test route using:

```python
await asyncio.sleep(10)
```

* Verified concurrent requests experimentally

---

# Important Concepts

## Blocking

Request waits and prevents other work.

Example:

```python
time.sleep(10)
```

---

## Non-blocking

Task pauses cooperatively and allows other tasks to execute.

Example:

```python
await asyncio.sleep(10)
```

---

## Event Loop

Central async scheduler that:

* pauses tasks
* resumes tasks
* manages concurrent coroutines

---

## Concurrency vs Parallelism

### Concurrency

Efficient handling of multiple tasks during waiting periods.

### Parallelism

Actual simultaneous CPU execution using multiple cores/processes.

---

## async def

Marks function as coroutine-capable.

Example:

```python
async def route():
```

---

## await

Cooperative pause point inside async function.

Example:

```python
await asyncio.sleep(5)
```

---

# Important Learning

Async improves:

```text
throughput
```

NOT:

```text
single request speed
```

---

# Important Insight

`async def` alone does NOT make everything async.

Internal libraries must also support async.

Example:

* `psycopg2` → synchronous
* `asyncpg` → asynchronous

---

# Major Learning

Shift from:

```text
“requests execute one-by-one”
```

toward:

```text
event-loop based concurrent request handling
```
