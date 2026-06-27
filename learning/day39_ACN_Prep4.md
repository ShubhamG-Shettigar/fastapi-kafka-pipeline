Microservices/EDA (Synchronous (REST) vs Asynchronous (Kafka), 
why Kafka instead of REST, 
-> In REST, its more like a request response model, hence it is synchronous. The client needs a response and the next steps / systems execute. THis leads to a delay in the overall operations.
hence, in asynchronous EDA, we use a model where the systems push events and then dont worry about the further actions. The ack of the published event is sent back to the source system.

-> In Monoliths, we just have 1 system. Everything and every logic is binded inside 1 code. This leads to tight coupling, increased code complexity, and complete blockage incase any 1 systems
fail. Whereas in microservices, we have independent systems meant for each operations like payments, orders, notifications, users, etc. So these modules behave independently and hence we have loose
coupling, meaning if payments stop, then orders would still work and payments once recovered would pick up the orders. 
 
N+1 query problem -> 
One event contains insufficient information, forcing downstream services to make additional queries to retrieve the missing data.
This is a problem in systems where we have to make N unneccesarry calls for a single event. Meaning if an event is published to some topic/db and there are N consumers 
reading from there, then all those N consumers make a REST call to the system where the actual data resides. This could be avoided by passing the actual data along with the event id, 
so that the 
N query is avoided. This pattern is called as Event-carried state transfer while the prior was called as Event Notifications.

EDA patterns
(1. Event notification (just events with id then make a REST call to get the actual data -> Leads to N+1 query problem),
2. Event-carried state transfer -> Pass event id and data together
3. Competing consumers -> Consumer group, consumer instances, 1 instance reads the event from each partition, no duplicate reads,
4. Publish-Subscribe (Pub-Sub)
A messaging pattern where a producer publishes an event to a topic, and all interested subscribers receive a copy independently. 
Kafka implements the Pub-Sub model while also supporting competing consumers through consumer groups.
### GCP Pub/Sub
A fully managed cloud-based Publish-Subscribe messaging service provided by Google Cloud for building asynchronous and event-driven applications.
### AWS EventBridge
An event routing service that receives events and forwards them to the appropriate downstream services (Lambda, SQS, SNS, Step Functions, etc.) based on configurable routing rules.
5. Request-Response using Kafka
Although Kafka is asynchronous, request-response can be implemented by publishing a request to one topic and the corresponding response to a reply topic 
using a **Correlation ID** to match the response with the original request.
6. CQRS (Command Query Responsibility Segregation)
CQRS separates the write (Command) and read (Query) operations into different models or databases, allowing each to be optimized and scaled independently according to workload.
### Eventual Consistency / Stale Reads
In CQRS with separate read and write models, the read model is updated asynchronously from the write model, resulting in temporary stale reads until synchronization completes.
7. Saga Pattern -> Compensating TXN -> Choreography and Orchestration modes (instead of Atomicity Rollback, invoke a new event to reverse the failed txn)
8. Outbox Pattern -> When business data must be written to a database and an event must be published to Kafka, performing both atomically is difficult because 
they involve different systems. The Outbox Pattern solves this by writing both the business record and an Outbox record within the same database transaction. 
A separate publisher later reads pending records from the Outbox table and publishes them to Kafka. 
If publishing fails, the event remains in the Outbox table and is retried later, ensuring reliable event delivery.)

EDA benefits
when not to use Kafka, 
Kafka vs Rabbit MQ vs SQS/SNS vs Redis PUB/Sub




