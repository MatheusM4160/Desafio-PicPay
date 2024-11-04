import sqlite3

conn = sqlite3.connect('register.db')
cursor = conn.cursor()

cursor.execute("""delete from client""")

conn.commit()