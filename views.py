import sqlite3 as sql
from main import app
from models import *
from flask import render_template, request, redirect, url_for

@app.route("/") 
def homepage():
    conn = sql.connect("banco.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Mes")
    tudo_mes = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("home.html", meses=tudo_mes) # enviando para o html, como reecebo no html?.

@app.route("/cadastro-gastos", methods=['GET']) 
def cadastrogastos():
    conn = sql.connect("banco.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM Gasto")
    nome_gasto = request.args.get('nome_gasto')
    valor_gasto = request.args.get('valor_gasto')

    cursor.execute(''' INSERT INTO Gasto (nome_gasto,valor_gasto)VALUES(?,?)''',(nome_gasto,valor_gasto))
    conn.commit()
    conn.close()
    return redirect(url_for('homepage')) 

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