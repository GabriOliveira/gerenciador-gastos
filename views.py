import sqlite3 as sql
from main import app
from models import *
from flask import render_template, request, redirect, url_for

@app.route("/", methods=["GET", "POST"]) 
def homepage():
    conn = sql.connect("banco.db")
    cursor = conn.cursor()
    botao = request.args.get("botao")

    if botao == "gasto":
            return render_template("cadastro-gasto.html")

    elif botao == "salario":
        return render_template("cadastro-salario.html")
    
            

    cursor.execute("SELECT nome_mes, COALESCE(salario, 0) FROM Mes ORDER BY id")
    campo_nome_mes_salario = cursor.fetchall()
    cursor.execute("SELECT nome_gasto, SUM(valor_gasto) FROM Gasto GROUP BY nome_gasto ORDER BY id")
    gastos_somados_nome_gasto = cursor.fetchall()
    cursor.execute("SELECT mes, sum(valor_gasto) FROM Gasto GROUP BY mes ORDER BY id")
    gastos_somados_mes = cursor.fetchall()

    cursor.close()

    conn.close()

    return render_template("home.html", campo_nome_mes_salario = campo_nome_mes_salario, gastos_somados_nome_gasto = gastos_somados_nome_gasto, gastos_somados_mes = gastos_somados_mes)

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
    
    conn.commit()
    cursor.close()
    conn.close()
    return render_template("home.html")

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
                
                return redirect(url_for("homepage")) 
        
    
        
    
    cursor.close()
    conn.close()

    return render_template('erro.html')

@app.route("/deletar-gasto", methods=['POST'])
def deletargasto():
    conn = sql.connect("banco.db")
    cursor = conn.cursor()
    
    botao = request.form.get("botao")
    
    if botao == "deletartodos":
        cursor.execute("DELETE FROM Gasto")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='Gasto'")
        conn.commit()
        return redirect(url_for('homepage'))

    elif botao == "deletarum":
        nome_gasto = request.form['nome_gasto']
        if nome_gasto:
            cursor.execute("DELETE FROM Gasto WHERE nome_gasto = ?", (nome_gasto,))
            conn.commit()
        return redirect(url_for('homepage'))
    else:
        return render_template("erro.html")
    cursor.close()
    conn.close()


# arrumar telas, atualizar views de cada tela, corrigir erro que nao atualiza a tabela, apenas atualiza após apertar o botão(fzr um form universal, onde cada tela tem ele com value diferente, e depnedendo do value ele executa um case q vai conter o codigo de sql para ver a tabela, switch = match)

#talvez Adição de categoria das dividas

#fazer uma tabela de quanto vai sobrar subtraindo as dividas do salario inteiro
#select na tabela gasto e pegar somente os valores que tem os meses em comum, e somar, 
# e exibir o resultado em cada mes na tabela Valor após gastos

#Organizar arquivos

#Tela Deletar salario e deletar gasto(deletar todos e deletar somente um)

# Aplicação de estilização(Bootstrap)
# fundo #214f4b 
# janelas #e0fbfc e #0dab76 
# letras #210b2c 

