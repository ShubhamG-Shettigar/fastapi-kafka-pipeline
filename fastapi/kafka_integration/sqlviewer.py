import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM shubham")
rows = cursor.fetchall()

for row in rows:
    print("Row 1",row)
    print()

cc = cursor.execute("Select count(*) from shubham").fetchone()[0]
print("Number of rows inserted till now:", cc)
conn.close()
