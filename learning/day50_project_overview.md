Our project is an Event-Driven Backend built around FastAPI, Kafka and PostgreSQL.

The application starts from main.py, which acts as the entry point of the FastAPI application and registers the different API routes. settings.py provides centralized configuration such as Kafka and PostgreSQL connection details, so these values do not need to be hardcoded throughout the application.

For authentication, the client interacts with auth_routes.py. These routes handle APIs such as signup and login. auth_routes.py uses schemas.py to validate incoming request data and uses auth_service.py for security-related operations such as password hashing, password verification and JWT creation/verification. When authentication data needs to be stored or retrieved, the route uses postgres.py to communicate with PostgreSQL. Therefore, auth_service.py handles security logic, while postgres.py handles database connectivity.

Once the user is authenticated, the same JWT can be used to access protected business APIs such as the future order API. Authentication and order processing are therefore separate responsibilities, but authentication can protect the order APIs.

For the event-driven part, order_routes.py will receive an order request and create a structured event using the event schema defined in schemas.py. The route then passes the event to producer.py. producer.py is responsible for serializing the event and publishing it to Kafka, primarily to the orders topic.

Kafka then acts as the event backbone of the application. The producer does not directly call the consumer or PostgreSQL. Instead, it publishes the event to Kafka, and consumer.py independently consumes that event using the orders_group consumer group.

consumer.py is responsible for consuming, deserializing and processing Kafka events. When an order event is successfully processed, it uses postgres.py to obtain a PostgreSQL connection and stores the required data in the orders table. After the database transaction succeeds, the consumer commits the Kafka offset. This gives us the basic at-least-once processing pattern.

If event processing fails, consumer.py does not contain all the retry logic itself. Instead, it delegates the failure to retryhandler.py. retryhandler.py checks the retry count. If the event is still eligible for retry, it publishes the event to the retry topic. The consumer consumes the retry event again. If the retry limit is exhausted, the event is published to the DLQ topic. This creates a retry → reprocess → DLQ flow without requiring a Python while loop.

metrics.py sits alongside the processing flow and provides Prometheus metrics such as successfully processed events, retry events and DLQ events. It does not participate in the business processing itself; it observes the system.

So the overall architecture can be thought of as four major areas:

1. API Layer
   main.py
   auth_routes.py
   order_routes.py

2. Business/Security Layer
   auth_service.py
   schemas.py

3. Infrastructure Layer
   settings.py
   postgres.py
   producer.py
   consumer.py
   retryhandler.py

4. Observability
   metrics.py

The most important architectural idea is that FastAPI does not directly control the entire workflow. FastAPI acts as one producer of events. Kafka becomes the communication backbone between producers and consumers, while PostgreSQL acts as the persistent data store.

Therefore, the eventual end-to-end order flow is:

Client
→ FastAPI
→ Authentication/JWT
→ Order API
→ Event Schema
→ Kafka Producer
→ Kafka orders topic
→ Kafka Consumer
→ PostgreSQL
→ Offset Commit

and on failure:

Kafka Consumer
→ Processing Failure
→ Retry Handler
→ Retry Topic
→ Consumer again
→ Retry exhausted
→ DLQ

This separation allows us to later add more producers, more consumers, different consumer groups, Redis, Schema Registry, Kafka Connect, Kafka Streams and other components without redesigning the entire application.