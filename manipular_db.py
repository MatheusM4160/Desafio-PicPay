import sqlite3

conn = sqlite3.connect('register.db')
cursor = conn.cursor()

cursor.execute("""drop table clientes""")

conn.commit()