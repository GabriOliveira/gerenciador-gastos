import sqlite3 as sql
from main import app
from models import *
from flask import render_template, request, redirect, url_for

@app.route("/", methods=["GET"]) 
def homepage():
    conn = sql.connect("banco.db")
    cursor = conn.cursor()
    
    botao = request.args.get("botao")
    if botao == "gasto":
      return  render_template("cadastro-gasto.html")
    elif botao == "salario":
      return  render_template("cadastro-salario.html")
    
    cursor.execute("SELECT nome_mes, COALESCE(salario, 0) FROM Mes ORDER BY id")
    campo_nome_mes_salario = cursor.fetchall()
    cursor.execute("SELECT mes, SUM(valor_gasto) FROM Gasto GROUP BY mes ORDER BY id")
    gastos_somados_mes = cursor.fetchall()
    cursor.execute("SELECT nome_gasto, SUM(valor_gasto) FROM Gasto GROUP BY nome_gasto ORDER BY id")
    gastos_somados_nome_gasto = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("home.html", campo_nome_mes_salario = campo_nome_mes_salario, gastos_somados_mes = gastos_somados_mes, gastos_somados_nome_gasto = gastos_somados_nome_gasto)

#PARTE DO MES(SALARIO)
@app.route('/cadastro-salario', methods=['POST'])
def cadastrosalario():
    conn = sql.connect("banco.db")
    cursor = conn.cursor()
    nome_mes = request.form.get('nome_mes_salario')
    salario = request.form.get('salario')

    if not salario or salario.strip() == "":
         cursor.close()
         conn.close()
         return render_template("erro.html")
    
    try:
        salario = float(salario)
    except ValueError:
        cursor.close()
        conn.close()
        return render_template("erro.html")
    
    cursor.execute(
            "UPDATE Mes SET salario = ? WHERE nome_mes = ?",
            (salario, nome_mes))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('homepage')) 

#PARTE DOS GASTOS
@app.route("/cadastro-gasto", methods=['POST']) 
def cadastrogastos():
    conn = sql.connect("banco.db")
    cursor = conn.cursor()

    #Obtem dados digitados pelo usuario e armazena em variaveis
    nome_mes =  request.form['nome_mes_gasto']
    nome_gasto = request.form['nome_gasto']
    valor_gasto = request.form['valor_gasto']

    if nome_gasto and valor_gasto:

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
                
                return redirect(url_for('homepage')) 
        #caso nao entre na condição, o contador é fechado e o usuário é direcionado a uma tela de erro
        conn.close()
    return render_template('erro.html')

@app.route('/deletar-gastos')
def deletargastos():
    conn = sql.connect("banco.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Gasto")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='Gasto'")
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('homepage')) 

@app.route('/deletar-salarios')
def deletarsalarios():

    conn = sql.connect("banco.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE Mes SET salario = NULL")
    conn.commit()
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='Mes'")
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('homepage')) 

@app.route('/deletar-um-gasto', methods=['POST'])
def deletargasto():
    conn = sql.connect("banco.db")
    cursor = conn.cursor()
    nome_gasto = request.form["nome_gasto"]

    if nome_gasto:
        cursor.execute("DELETE FROM Gasto WHERE nome_gasto = ?", (nome_gasto,))
        conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('homepage')) 
    
@app.route('/deletar-um-salario')
def deletarsalario():
    conn = sql.connect("banco.db")
    cursor = conn.cursor()
    
    

    conn.commit()
    cursor.close()
    conn.close()
    