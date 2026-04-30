import sqlite3 as sql

conn = sql.connect("banco.db")
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS Mes (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            nome_mes TEXT NOT NULL UNIQUE,
            salario FLOAT
               )""")
cursor.execute("""CREATE TABLE IF NOT EXISTS Gasto (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            nome_gasto TEXT NOT NULL,
            valor_gasto FLOAT NOT NULL,
            mes TEXT NOT NULL
               )""")

conn.commit()
cursor.close()
conn.close()
