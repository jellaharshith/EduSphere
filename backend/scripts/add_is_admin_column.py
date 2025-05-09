import sqlite3

conn = sqlite3.connect("edusphere.db")
cursor = conn.cursor()
try:
    cursor.execute("ALTER TABLE user ADD COLUMN is_admin BOOLEAN DEFAULT 0;")
    print("Added is_admin column to user table.")
except Exception as e:
    print(f"Error: {e}")
conn.commit()
conn.close() 