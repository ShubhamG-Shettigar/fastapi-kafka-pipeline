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
    cursor = connection.cursor()
    try:
        yield cursor
    finally:
        cursor.close()
        connection.close()

def get_cursor():
    connection = get_connection()
    return connection.cursor()