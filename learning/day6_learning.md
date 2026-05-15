# Day 6 Learning 🚀

## Topics Covered
- PostgreSQL installation and verification
- psql shell usage
- Server-based DB architecture
- Embedded DB vs Relational DB Server
- UUID constraints
- Python ↔ PostgreSQL connection
- psycopg2 driver
- PostgreSQL authentication model

---

# PostgreSQL Installation

Successfully installed PostgreSQL locally on Windows.

Verified PostgreSQL service through:

services.msc

Observed:
- PostgreSQL runs as an independent database service
- Unlike SQLite, PostgreSQL is not file-based from application perspective

---

# PostgreSQL Shell (psql)

Connected successfully using:

```bash
psql -U postgres