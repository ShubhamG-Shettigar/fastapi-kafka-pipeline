1. Basic FastAPI -> Kafka-> DB
2. DB insert + commit -> then Kafka failure -> causes duplicacy at the db when retried -> Can be eliminated using unique identifier (UUID message id)
3. Kafka commit before DB commit -> Possible chances of data loss
4. Replace auto.commit with manual sync commit (consumer.commit())
5. Idempotent consumer pattern, where repeated processing of the same event does not create duplicate effects.
6. Migrated to PostgreSQL. Tried multiple consumers, multiple partitions (sticky partitioning)