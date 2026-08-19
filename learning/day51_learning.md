# Backend Switch — Day 51

## Date
19 August 2026

## Day 51 Summary

### Completed
- Cleaned `main.py` — now responsible mainly for FastAPI app creation, router registration and `create_orders_table()`.
- Removed unused `/protected` test endpoint.
- Created and registered `order_routes.py`.
- Added `OrderRequest` schema:
  - `order_id`
  - `customer_name`
  - `amount`
- Added/used `EventEnvelope` schema:
  - `event_id`
  - `event_type`
  - `event_version`
  - `timestamp`
  - `source`
  - `payload`
- Implemented Order → EventEnvelope conversion inside `order_routes.py`.
- Used `event.model_dump(mode="json")` because `datetime` is not directly JSON serializable.
- Verified complete EventEnvelope reaches Kafka `orders` topic.
- Verified Kafka console consumer and Python `consumer.py` are independent consumers; different consumer groups can consume the same event.
- Confirmed Kafka records persist according to retention and consumer offsets are independent.
- Confirmed `consumer.commit()` is synchronous; `consumer.commit_async()` is asynchronous.
- Consumer now consumes both `orders` and `orders-retry`.
- Consumer successfully extracted `data["payload"]` and inserted orders into PostgreSQL.
- Verified `orders` table contains the consumed event.
- Verified DB transaction is committed before Kafka offset is committed.
- Tested retry/DLQ flow successfully.

### Retry/DLQ Test

Temporary failure:

```python
raise Exception("Testing retry and DLQ flow")