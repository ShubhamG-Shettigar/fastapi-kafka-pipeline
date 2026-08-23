import psycopg2
from app.configs.settings import settings

def get_connection():
    return psycopg2.connect(
        host=settings.postgres_host,
        database=settings.postgres_db,
        user=settings.postgres_user,
        password=settings.postgres_password,
        port=settings.postgres_port
    )

def get_db():
    connection = get_connection()
    try:
        yield connection
    finally:
        connection.close()

def create_orders_table():
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id SERIAL PRIMARY KEY,
                event_id VARCHAR(100) UNIQUE NOT NULL,
                order_id VARCHAR(100) UNIQUE NOT NULL,
                customer_name VARCHAR(100) NOT NULL,
                amount NUMERIC(10, 2) NOT NULL
                )
        """)
        
        connection.commit()
    finally:
        cursor.close()
        connection.close()