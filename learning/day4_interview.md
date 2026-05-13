# Interview Scenario - Graceful Duplicate Replay Handling

## Question

A Kafka consumer uses idempotent processing with a UNIQUE message_id in the database.

When Kafka re-delivers an already processed message:
- DB raises duplicate constraint exception
- Consumer safely ignores duplicate
- Offset is committed

Why is this considered correct behavior?

---

## Answer

Kafka provides at-least-once delivery, so duplicate message delivery is expected during crash recovery scenarios.

Since the message was already processed earlier, the duplicate replay is not a real failure.

The consumer detects the duplicate using the UNIQUE message_id constraint, safely ignores the duplicate insert, and commits the offset intentionally.

This is called idempotent consumer design with graceful duplicate handling.