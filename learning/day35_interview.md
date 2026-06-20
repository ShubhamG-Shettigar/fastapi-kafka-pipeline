# interview.md — Day 35 (Pre-OA Light Revision)

## Topic: Kafka Consumer Groups & Rebalancing

### Scenario

Topic: orders

Partitions: 6

Consumer Group:

3 Consumer Instances

One consumer crashes.

---

## What Happens After Consumer Crash?

Flow:

Consumer Crash
↓
Group Coordinator Detects Failure
↓
Rebalance Triggered
↓
Partitions Reassigned
↓
Consumption Resumes

Learning:

Kafka automatically redistributes partitions owned by the failed consumer among remaining active consumers.

---

## What Is Rebalance?

Definition:

Process where Kafka revokes existing partition assignments and redistributes partitions among active consumers in the group.

Important:

* Existing assignments are revoked.
* New assignments are created.
* Consumption pauses temporarily during rebalance.

---

## Impact Of Rebalance

During rebalance:

* No active message consumption.
* Throughput temporarily drops.
* Consumer lag may increase.

---

## Why Frequent Rebalances Are Bad

Consumers spend time:

* Leaving group
* Joining group
* Reassigning partitions

instead of:

* Polling
* Processing messages

Result:

Reduced throughput and unstable consumer group behavior.

---

## Consumer Count vs Partition Count

Question:

6 Partitions
10 Consumers

How many consumers receive data?

Answer:

Only 6 consumers.

Reason:

A partition can be assigned to at most one consumer within a consumer group.

Remaining 4 consumers stay idle.

---

## Important Interview Rule

Maximum Parallelism = Number of Partitions

Examples:

6 Partitions + 3 Consumers
→ 3 Active Consumers

6 Partitions + 6 Consumers
→ 6 Active Consumers

6 Partitions + 10 Consumers
→ 6 Active Consumers + 4 Idle Consumers

Learning:

Increasing consumers beyond partition count does not increase throughput.

Partitions determine parallelism.

---
