from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Application
    app_name: str = "Event Driven Backend"

    # Kafka
    kafka_bootstrap_servers: str = "localhost:9092"
    kafka_orders_topic: str = "orders"
    kafka_retry_topic: str = "orders-retry"
    kafka_dlq_topic: str = "orders-dlq"

    # PostgreSQL
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "kafka_project"
    postgres_user: str = "postgres"
    postgres_password: str = "postgresql"

    class Config:
        env_file = ".env"


settings = Settings()