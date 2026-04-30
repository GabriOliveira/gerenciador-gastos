from views import *

conn = sql.connect("banco.db")
cursor = conn.cursor()

#cursor.execute('''DROP TABLE Gasto''')
#cursor.execute('''DROP TABLE Mes''')

cursor.execute('''SELECT * FROM Gasto''')
tudo = cursor.fetchall()
print(tudo)

conn.commit()
cursor.close()
conn.close()