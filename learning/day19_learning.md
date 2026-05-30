# Day 19 - Transactions, Concurrency & Background Tasks

## Transactions

A transaction is a group of DB operations that either:

* fully succeed
  OR
* fully fail

### Important Commands

* `commit()` → permanently save changes
* `rollback()` → undo changes

Without `commit()`, PostgreSQL auto-rolls back changes when connection closes.

---

## ACID Properties

### A → Atomicity

All operations succeed together or fail together.

### C → Consistency

DB should always remain in valid state.

### I → Isolation

Concurrent transactions should not corrupt each other.

### D → Durability

After commit, data survives crashes/restarts.

---

## Important Production Rule

After DB exception:

```python
conn.rollback()
```

Otherwise transaction may remain in failed state.

Example error:

```text
current transaction is aborted
```

---

## Autocommit

PostgreSQL default:

```text
autocommit = OFF
```

Meaning changes are temporary until explicit commit.

Reason:

* allows multi-step transactions safely.

---

## Concurrency & Booking Systems

### Problem

Multiple users booking same seat simultaneously.

### Common Solutions

* Row-level locking
* Atomic updates
* Queues
* Reservation systems
* Rate limiting

### Important Insight

Large systems prioritize:

```text
correct booking > perfectly real-time UI
```

---

## Reservation vs Lock

### DB Lock

Very short-lived.
Held until commit/rollback.

### Reservation

Business-level temporary hold.
Example:

```text
Seat reserved for 2 mins
```

---

## Background Tasks (FastAPI)

Used for:

* emails
* notifications
* logging
* analytics
* async side work

Concept:
Return API response immediately, do extra work later.

Example:

```python
background_tasks.add_task(send_email)
```

Important:

```python
send_email
```

passes function reference.

NOT:

```python
send_email()
```

---

## Biggest Learning Today

Backend engineering is not only APIs.

Real systems focus heavily on:

* consistency
* concurrency
* coordination
* scaling
* failure handling
