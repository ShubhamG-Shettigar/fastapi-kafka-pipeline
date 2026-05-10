You have a Kafka consumer that:
Consumes message
Inserts into DB
Crashed BEFORE committing Kafka offset

After restart, the same message is processed again and DB shows duplicates.

❓ Questions
Why did duplicate data happen?
What Kafka guarantee caused this behavior?
How would you design the system to prevent duplicates?


Answer

Duplicates happened due to at-least-once delivery.
Since offset was not committed before crash, Kafka re-delivered the message.
We prevent this using idempotency at the consumer/DB level.