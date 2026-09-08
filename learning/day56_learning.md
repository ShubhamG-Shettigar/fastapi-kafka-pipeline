# Day 56 — Status Event Retry & DLQ

## Done

* Resumed Backend Switch after a break and revised the existing architecture.
* Confirmed two Kafka consumers:

  * Orders Consumer
  * Order Status Consumer
* Added dedicated status-event retry and DLQ topics:

  * `order-status-retry`
  * `order-status-dlq`
* Refactored `handle_failure()` to accept retry/DLQ topics as parameters instead of hardcoding `orders-retry` and `orders-dlq`.
* Updated `order_status_consumer.py` to use the generic failure handler.
* Updated Status Consumer to consume from both:

  * `order-status-events`
  * `order-status-retry`

## Architecture

```text
orders
orders-retry
orders-dlq
    ↓
Orders Consumer
    ↓
PostgreSQL


order-status-events
order-status-retry
order-status-dlq
    ↓
Order Status Consumer
    ↓
PostgreSQL
```

## Retry Flow

```text
order-status-events
        ↓
Status Consumer
        ↓
DB processing fails
        ↓
order-status-retry
        ↓
Same Status Consumer
        ↓
Success → PostgreSQL
   OR
Failure → order-status-dlq
```

`MAX_RETRIES = 1`, so only one retry attempt is made before moving the event to DLQ.

## Verified

* Status event successfully moved to retry topic after DB failure.
* Retry attempt was processed by the same Status Consumer.
* After retry failure, event moved to `order-status-dlq`.
* DLQ event verified in Kafka.
* Database remained unchanged after failed processing.
* Confirmed that Kafka retains the original event and retry copy in their respective topics.
* Confirmed manual KRaft topic recreation after Kafka metadata/topic loss.

## Key Learning

`event_id` remains the identity of the event even when the event is copied to a retry topic.

The original event and retry record can therefore have the same `event_id` while existing in different Kafka topics.

## Day 56 Status

**Retry/DLQ handling for order-status events — COMPLETE ✅**

## Next

* Review overall project architecture and current progress.
* Decide the next development phase.
* Eventually extend order lifecycle:
  `CREATED → CONFIRMED → SHIPPED → DELIVERED`
* Continue production-style improvements without unnecessarily increasing architectural complexity.
