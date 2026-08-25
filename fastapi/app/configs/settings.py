from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Application
    app_name: str = "Event Driven Backend"

    # Kafka
    kafka_bootstrap_servers: str = "localhost:9092"
    kafka_orders_topic: str = "orders"
    kafka_retry_topic: str = "orders-retry"
    kafka_dlq_topic: str = "orders-dlq"
    kafka_order_status_topic: str = "order-status-events"

    # PostgreSQL
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "kafka_project"
    postgres_user: str = "postgres"
    postgres_password: str = "postgresql"
    
    # JWT
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"


settings = Settings()