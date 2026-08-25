# Day 55 — Order Lifecycle & Status Events

## Done

* Added `status` column to `orders` table with default `CREATED`.
* Added Kafka topic: `order-status-events`.
* Added `/orders/{order_id}/confirm` API.
* Added `ORDER_CONFIRMED` event publishing.
* Added separate `order_status_consumer.py`.
* Consumer updates PostgreSQL order status asynchronously.
* Added order ownership validation using `user_id`.
* Added valid status lifecycle:
  `CREATED → CONFIRMED → SHIPPED → DELIVERED`
* Added cancellation support for `CREATED` / `CONFIRMED`.
* Added transition validation to prevent invalid jumps/repeats.

## Verified

* `CREATED → CONFIRMED` ✅
* `CONFIRMED → CONFIRMED` → `400 Invalid status transition` ❌
* Different user's order cannot be modified ✅
* Kafka event ID remains unique while `order_id` remains the order identity.
* JWT expiry and protected endpoints verified.

## Architecture

`API → Kafka → Status Consumer → PostgreSQL`

## Next

* Extend lifecycle to `SHIPPED` and `DELIVERED`.
* Handle status-event retry/DLQ properly.
* Continue production-style improvements.
