# Kafka Interview Learnings

1. Idempotence avoids duplicate writes from the same producer.
2. Transactions = Atomic writes across partitions.
3. Kafka Streams EOS = Transactions + Consumer Offset Commit.
4. Event-carried State Transfer reduces N+1 REST calls.
5. Outbox Pattern solves DB + Kafka atomicity.