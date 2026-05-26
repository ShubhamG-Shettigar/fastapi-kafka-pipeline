# Day 15 — Backend Modularization

## Completed

* Created `routes/` folder
* Created `auth_routes.py`
* Introduced `APIRouter`
* Moved `/signup` and `/login` routes out of `main.py`
* Registered router using:

```python
app.include_router(auth_router)
```

* Added route prefix:

```python
prefix="/auth"
```

Result:

```text
/auth/signup
/auth/login
```

* Created:

```python
def get_cursor():
    return conn.cursor()
```

* Switched from global cursor reuse to fresh cursor per request

---

## Important Concepts

### APIRouter

Used for modular route grouping.

Instead of keeping all APIs in `main.py`, routes are separated into domain-specific files.

---

### Connection vs Cursor

#### Connection

Long-lived communication tunnel to DB.

```python
conn = psycopg2.connect(...)
```

#### Cursor

Executes SQL queries using connection.

```python
cursor.execute(...)
```

Fresh cursor per request is cleaner and safer.

---

### Trigger

Automatic DB-side action on some event.

Example:

* insert user
* auto-create audit log

---

### Python Import Behavior

Importing a file executes entire file top-to-bottom.

---

## Current Architecture

```text
app/
 ├── main.py
 ├── routes/
 │    ├── auth_routes.py
 ├── services/
 │    ├── auth.py
 ├── db/
 │    ├── postgres.py
```

---

## Major Learning

Shift from:

```text
single-file coding
```

toward:

```text
modular backend architecture
```
