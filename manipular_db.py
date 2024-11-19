import sqlite3

conn = sqlite3.connect('register.db')
cursor = conn.cursor()

cursor.execute("""ALTER TABLE account ADD password int(6)""")

conn.commit()