import sqlite3

con = sqlite3.connect('database.db')
print("Opened database successfully")

cur = con.cursor()
cur.execute('''CREATE TABLE PREDICTIONS(ID INTEGER PRIMARY KEY AUTOINCREMENT, NAME TEXT NOT NULL, FILE TEXT NOT NULL, DATE TEXT NOT NULL, RESULT TEXT NOT NULL)''')
print("Table created successfully")

con.commit()
con.close()