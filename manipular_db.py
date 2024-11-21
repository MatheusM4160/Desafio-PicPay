import sqlite3

conn = sqlite3.connect('register.db')
cursor = conn.cursor()

cursor.execute("""CREATE TABLE transaction_history (
               id_client INT,
               give INT,
               get INT,
               date TEXT(10))""")

conn.commit()