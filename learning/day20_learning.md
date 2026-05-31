# Day 20 - Backend Architecture & Transaction Flow

## Layered Architecture

We separated backend into layers:

### Route Layer

Responsibilities:

* request handling
* response handling
* orchestration
* transaction control

### Service Layer

Responsibilities:

* business logic
* reusable operations

### Models Layer

Responsibilities:

* request/response schemas
* data validation contracts

---

## Current Project Structure

```text
routes/
services/
models/
postgres/
```

Project is now transitioning from tutorial-style code toward maintainable backend architecture.

---

## Service Refactor

Moved signup business logic into:

```python
create_user()
```

inside:

```text
services/auth_service.py
```

Benefits:

* reusable logic
* cleaner routes
* scalable structure
* easier maintenance

---

## Transaction Ownership

Two architecture patterns discussed:

### Pattern 1

Route controls:

* commit
* rollback

Service controls:

* business logic

### Pattern 2

Service controls:

* business logic
* transaction lifecycle

Important Learning:
There is no universally correct architecture.
Tradeoffs matter.

Current project continues with:

```text
Route owns transaction control
```

---

## Pydantic Response Models

Created:

```python
class MessageResponse(BaseModel):
    message: str
```

Used with:

```python
response_model=MessageResponse
```

Important Insight:
Pydantic validates:

* dictionary structure
* required keys
* value data types

Example valid response:

```python
return {"message":"success"}
```

Invalid:

```python
return "success"
```

because schema expects:

```python
{
   "message": <string>
}
```

---

## HTTPException

Introduced proper API error handling:

```python
raise HTTPException(
    status_code=400,
    detail="Username already exists"
)
```

Important Insight:
HTTP status codes are part of API contract.

---

## Specific vs Generic Exceptions

Used:

```python
except UniqueViolation:
```

before:

```python
except Exception:
```

Reason:
Specific exceptions must be caught before generic exceptions.

---

## Dependency Injection Lifecycle

Dependency example:

```python
def get_db():

    cursor = conn.cursor()

    try:
        yield cursor

    finally:
        cursor.close()
```

Flow:

1. Request arrives
2. Cursor created
3. Cursor yielded to route
4. Route executes
5. Control returns after yield
6. finally block runs
7. Cursor closes automatically

Important:
`finally` executes after request lifecycle ends.

---

## Atomicity Experiment (VERY IMPORTANT)

Experiment:

* duplicated INSERT query
* first insert succeeded
* second insert failed
* rollback executed

Result:
NO rows persisted.

This demonstrated:

```text
Atomicity (A in ACID)
```

Meaning:
Transaction fully succeeds OR fully fails.

Even successful earlier queries disappear if rollback occurs before commit.

---

## Biggest Learning Today

Good architecture is not about:

```text
“maximum abstraction”
```

Good architecture is about:

```text
clarity + maintainability + scalability
```

Over-engineering can reduce readability instead of improving design.
