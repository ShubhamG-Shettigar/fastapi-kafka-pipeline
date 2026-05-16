# Interview Notes - Day 7 🚀

## Kafka Consumer Groups and Partitions

### Q1. If a Kafka topic has 3 partitions and a consumer group has 4 consumers, how many consumers actively process messages?

Only 3 consumers actively process messages because maximum parallelism in a Kafka consumer group depends on the number of partitions.

One partition can only be assigned to one consumer within the same consumer group.

The 4th consumer remains idle.

---

## Q2. Why can’t multiple consumers from the same group consume the same partition simultaneously?

Because Kafka guarantees ordering within a partition.

If multiple consumers consume the same partition simultaneously:

* ordering guarantees break
* offset consistency issues occur
* duplicate/out-of-order processing may happen

Kafka group coordinator therefore ensures:

* one partition → one active consumer (per group)

---

## Q3. What happens when a new consumer joins or leaves a consumer group?

Kafka triggers a rebalance.

During rebalance:

* partitions may be reassigned
* consumer ownership changes dynamically
* group coordinator updates metadata

Rebalance also happens if:

* heartbeat fails
* session timeout occurs
* consumer crashes unexpectedly

---

## Q4. What is sticky partition assignment?

Modern Kafka consumers use sticky assignment strategy.

Goal:

* minimize unnecessary partition movement during rebalance
* preserve previous assignments as much as possible

However:

* sticky assignment is best-effort
* partition ownership can still change if balancing requires it

---

## Q5. What is the relationship between partitions and scalability?

Kafka scalability depends on partitions.

Maximum parallel consumer processing inside one consumer group equals:

* number of partitions

More partitions allow:

* higher parallelism
* distributed consumption
* horizontal scaling
