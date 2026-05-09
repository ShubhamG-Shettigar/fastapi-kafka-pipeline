import sqlite3
conn = sqlite3.connect("items.db")
cursor = conn.cursor()


cursor.execute("Delete from shubham")
print("Items were deleted")
conn.commit()