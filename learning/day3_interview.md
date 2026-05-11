# Interview Scenario - Idempotent Kafka Consumer

## Question

A Kafka consumer crashes after inserting data into DB but before committing Kafka offset.

After restart:
- Kafka re-delivers the same message
- But duplicate DB records are not created.

Explain:
1. Why Kafka re-delivered the message
2. How duplicates were prevented
3. Which design pattern is being used

---

## Answer

Kafka re-delivered the message because the consumer crashed before committing the offset, so Kafka considered the message unprocessed.

Duplicates were prevented using a unique message_id stored in the database with a UNIQUE constraint.

This design pattern is called an idempotent consumer pattern, where repeated processing of the same event does not create duplicate effects.