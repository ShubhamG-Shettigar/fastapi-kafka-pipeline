import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="kafka_project",
    user="postgres",
    password="postgresql",
    port="5432"
)

print("Connected to PostgreSQL successfully!")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS test_users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100)
)
""")

conn.commit()

print("Table created successfully!")

cursor.close()
conn.close()

print("Connection closed.")
