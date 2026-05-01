import sqlite3 as sql
from main import app
from models import *
from flask import render_template, request, redirect, url_for

@app.route("/") 
def homepage():
    conn = sql.connect("banco.db")
    cursor = conn.cursor()
    cursor.execute("SELECT nome_mes FROM Mes ORDER BY id")
    tabela_mes = cursor.fetchall()
    cursor.execute("SELECT salario FROM Mes  ORDER BY id")
    tabela_salario = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template("home.html", tabela_mes = tabela_mes, tabela_salario = tabela_salario)

@app.route("/cadastro", methods=['GET']) 
def cadastrogastos():
    conn = sql.connect("banco.db")
    cursor = conn.cursor()

    #Obtem dados digitados pelo usuario e armazena em variaveis
    nome_mes =  request.args.get('nome_mes')#.lower
    salario = request.args.get('salario')

    nome_gasto = request.args.get('nome_gasto')#.lower
    valor_gasto = request.args.get('valor_gasto')

    #Obtem todos valores nome_mes cadastrados no BD
    cursor.execute('''SELECT nome_mes FROM Mes''')
    meses_cadastrados = cursor.fetchall()
    
    #Percorre cada valor dos valores anteriores obtidos e executa o IF
    for meses in meses_cadastrados:
        if meses[0] == nome_mes:
            cursor.execute(
            "INSERT INTO Gasto (nome_gasto, valor_gasto, mes) VALUES (?, ?, (SELECT nome_mes FROM Mes WHERE nome_mes = ?))",
            (nome_gasto, valor_gasto, nome_mes)
        )
            conn.commit()

            cursor.execute(
            "UPDATE Mes SET salario = ? WHERE nome_mes = ?",
            (salario, nome_mes)
        )
            conn.commit()    
            return redirect(url_for('homepage')) 
    #caso nao entre na condição, o contador é fechado e o usuário é direcionado a uma tela de erro
    conn.close()
    return render_template('erro.html')

@app.route("/alterar-salario")
def alterarsalario():
    conn = sql.connect("banco.db")
    cursor = conn.cursor()
    cursor.close()
    conn.close()
    return "alterar salario"

@app.route("/ver-gastos") 
def vergastos():
    conn = sql.connect("banco.db")
    cursor = conn.cursor()
    cursor.close()
    conn.close()
    return "ver gastos"

@app.route('/deletar-gastos')
def deletar():
    conn = sql.connect("banco.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Gasto")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='Gasto'")
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('homepage')) 