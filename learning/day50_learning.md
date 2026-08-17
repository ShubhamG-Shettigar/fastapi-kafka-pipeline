# Backend Switch — Day 50 Checkpoint

## Day 50 Goal

Continue the Phase 1 architecture refactor and establish a clean, working baseline for the Event-Driven Backend.

---

## Work Completed

### 1. settings.py

Centralized application configuration using `pydantic-settings`.

Responsibilities:

- Application configuration
- Kafka configuration
- PostgreSQL configuration
- `.env` support

Important concept:

- `Settings` = configuration class/blueprint
- `settings` = instantiated configuration object

---

### 2. postgres.py

Refactored PostgreSQL access.

Current responsibilities:

- Create PostgreSQL connections
- Provide FastAPI DB dependency
- Initialize the `orders` table

Current functions:

- `get_connection()`
- `get_db()`
- `create_orders_table()`

Important design:

- No global PostgreSQL connection
- No global cursor
- Each operation manages its own DB resources
- FastAPI receives a connection through `get_db()`
- Kafka consumer explicitly obtains a connection using `get_connection()`

---

### 3. producer.py

Refactored Kafka producer boundary.

Responsibilities:

- Create Kafka producer
- Serialize Python event data into JSON
- Publish event to a specified Kafka topic

Current architecture:

Application
    ↓
publish_event()
    ↓
KafkaProducer
    ↓
Kafka topic

Producer reliability topics are postponed to Phase 2:

- acks
- retries
- idempotent producer
- ordering
- batching

---

### 4. schemas.py

Existing API schemas retained:

- UserSignup
- UserLogin
- User
- MessageResponse

Event-driven architecture foundation added:

- EventEnvelope

EventEnvelope concept:

- event_id
- event_type
- event_version
- timestamp
- source
- payload

This will later support:

- Complex events
- Nested payloads
- Multiple event types
- Schema Registry
- Schema evolution

---

### 5. consumer.py

Consumer refactored from the old large implementation.

Current responsibilities:

- Consume Kafka events
- Deserialize JSON
- Process events
- Call PostgreSQL
- Increment successful-processing metric
- Commit Kafka offsets
- Call retry handler when processing fails

Consumer group:

`orders_group`

Topics consumed:

- orders
- orders-retry

Current success flow:

Kafka event
    ↓
Consumer
    ↓
PostgreSQL
    ↓
DB commit
    ↓
processed_events_total.inc()
    ↓
Kafka offset commit

Current failure flow:

Consumer
    ↓
Processing failure
    ↓
retryhandler
    ↓
orders-retry OR orders-dlq

---

### 6. retryhandler.py

Created a dedicated retry/DLQ boundary.

Current configuration:

`MAX_RETRIES = 1`

Logic:

retry_count < MAX_RETRIES
    ↓
retry topic

retry_count >= MAX_RETRIES
    ↓
DLQ topic

Topics:

- orders-retry
- orders-dlq

Important concept:

There is no `while` loop in retryhandler.

Retry attempts happen because Kafka sends the retry event back to the consumer.

Example:

orders
    ↓
failure
    ↓
orders-retry
    ↓
consumer
    ↓
failure
    ↓
orders-dlq

Metrics added:

- retry_events_total
- dlq_events_total

---

### 7. auth_service.py

Cleaned authentication service.

Responsibilities:

- Password hashing
- Password verification
- JWT creation
- JWT verification

Functions:

- hash_password()
- verify_password()
- create_access_token()
- verify_token()

Removed:

- PostgreSQL imports
- create_user()
- direct database persistence

Important architecture decision:

`auth_service.py` should NOT own PostgreSQL persistence.

---

### 8. auth_routes.py

Cleaned authentication routes.

Responsibilities:

- HTTP authentication endpoints
- Request validation
- Database interaction for authentication data
- Calling auth_service for security operations

Current endpoints:

- POST /auth/signup
- POST /auth/login

Signup:

HTTP request
    ↓
auth_routes
    ↓
hash_password()
    ↓
PostgreSQL auth_users
    ↓
commit
    ↓
response

Login:

HTTP request
    ↓
auth_routes
    ↓
PostgreSQL auth_users
    ↓
stored password hash
    ↓
verify_password()
    ↓
create_access_token()
    ↓
JWT response

Removed old experiments:

- BackgroundTasks email experiment
- async test endpoint
- Kafka signup publishing
- old get_cursor()
- global DB connection usage

---

### 9. main.py

Cleaned application entry point.

Responsibilities:

- Create FastAPI application
- Initialize orders table
- Register routers

Current router:

- auth_router

The old `/send` Kafka experiment was removed.

The proper order API will be created separately.

---

### 10. metrics.py

Prometheus metrics retained.

Current metrics:

- processed_events_total
- retry_events_total
- dlq_events_total
- consumer_lag

These will support observability later.

---

## Kafka Topics

Old experimental topics preserved:

- signup-events
- signup-events-retry
- signup-events-dlq

New event-driven topics created:

- orders
- orders-retry
- orders-dlq

Each new topic has:

- 3 partitions
- replication factor 1 (single local broker)

---

## PostgreSQL

Existing tables preserved:

- auth_users
- dlq_users
- test_users
- users

New table created:

- orders

Current orders table:

- id
- order_id
- customer_name
- amount

`order_id` is UNIQUE to support future DB-side idempotency.

---

## Runtime Status at End of Day 50

Kafka broker:
RUNNING

Kafka consumer:
RUNNING

Uvicorn:
RUNNING

PostgreSQL:
RUNNING

orders topic:
READY

orders-retry topic:
READY

orders-dlq topic:
READY

orders table:
CREATED SUCCESSFULLY

---

## Current Architecture

                    FastAPI
                       |
             +---------+---------+
             |                   |
       auth_routes          future order_routes
             |                   |
       auth_service              |
             |                   |
        PostgreSQL               ↓
        auth_users             Kafka
                                |
                         +------+------+
                         |             |
                      orders      orders-retry
                         |             |
                         +------+------+
                                |
                             consumer
                                |
                           PostgreSQL
                              orders

---

## Remaining Phase 1 Work

1. Create order_routes.py
2. Connect EventEnvelope to order API
3. Publish ORDER_CREATED events
4. Test Kafka → Consumer → PostgreSQL
5. Test retry flow
6. Test DLQ flow
7. Final architecture review
8. Establish stable working baseline

---

## Next Session — Day 51

Start with:

`app/models/schemas.py`

Verify the current EventEnvelope definition.

Then create:

`app/routes/order_routes.py`

Target first end-to-end flow:

FastAPI
    ↓
EventEnvelope
    ↓
producer.py
    ↓
orders topic
    ↓
consumer.py
    ↓
orders table

After that, deliberately test:

SUCCESS
    → DB commit
    → Kafka offset commit

FAILURE
    → retry topic
    → retry processing
    → DLQ after retry limit

---

## Day 50 Key Learning

The major focus was separation of responsibilities.

settings.py
→ configuration

postgres.py
→ database connection boundary

schemas.py
→ data/event structure

producer.py
→ Kafka publishing

consumer.py
→ Kafka consumption and processing flow

retryhandler.py
→ retry/DLQ handling

auth_service.py
→ authentication/security logic

auth_routes.py
→ authentication HTTP endpoints

main.py
→ FastAPI application entry point

metrics.py
→ observability

The project is now moving from:

"FastAPI application that happens to use Kafka"

towards:

"Event-driven backend where FastAPI is one of the producers."