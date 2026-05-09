# Day 1 Interview Scenario 🎯

## Scenario
Producer successfully sends message to Kafka. Consumer reads message. Database insert succeeds.
BUT consumer crashes BEFORE offset commit.

---

## Questions

1. Will the same message be consumed again after restart?
2. What issue can happen in downstream systems?
3. What processing semantic does this represent?

---

## Answer

Yes.
Kafka consumer resumes from the last committed offset.
Since offset was not committed before the crash, the same message will be consumed again after restart.
This can lead to duplicate processing such as:
- duplicate DB rows
- duplicate notifications
- duplicate payments

This behavior is part of:
At-least-once processing semantics

Meaning:
Messages may be processed more than once, but should not be lost.

Real-world systems solve this using:
- idempotency
- deduplication
- transactional workflows