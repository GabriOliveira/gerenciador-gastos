import sqlite3 as sql

conn = sql.connect("banco.db")
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS Mes (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            nome_mes TEXT NOT NULL UNIQUE,
            salario TEXT
               )""")
cursor.execute("""CREATE TABLE IF NOT EXISTS Gasto (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            nome_gasto TEXT NOT NULL,
            valor_gasto FLOAT NOT NULL,
            mes TEXT NOT NULL
               )""")
#Insere os meses em por meio de uma lista de tuplas
meses_fixos = [
        ('Janeiro',),
        ( 'Fevereiro',),
        ( 'Março',),
         ('Abril',),
         ('Maio',),
         ('Junho',),
         ('Julho',),
        ( 'Agosto',),
         ('Setembro',),
         ('Outubro',),
        ( 'Novembro',),
         ('Dezembro',)
    ]
cursor.executemany(''' INSERT OR IGNORE INTO Mes (nome_mes)VALUES(?)''',(meses_fixos))
conn.commit()
cursor.close()
conn.close()
