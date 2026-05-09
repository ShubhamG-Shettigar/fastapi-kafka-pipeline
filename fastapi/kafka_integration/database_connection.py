import sqlite3

# DB connect (agar file nahi hai to create ho jayegi)
conn = sqlite3.connect("users.db")

# cursor object
cursor = conn.cursor()

# table create (agar already nahi hai to)
cursor.execute("""
CREATE TABLE IF NOT EXISTS shubham (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    surname TEXT
)
""")

# save changes
conn.commit()
