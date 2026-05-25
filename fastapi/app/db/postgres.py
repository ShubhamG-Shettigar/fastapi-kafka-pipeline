import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="kafka_project",
    user="postgres",
    password="postgresql",
    port="5432"
)

#print("Connected to PostgreSQL successfully!")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS auth_users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
)
""")

conn.commit()

#print("Table created successfully!")

#cursor.close()
#conn.close()

#print("Connection closed.")
