







# Importa as funções necessárias do Flask
from flask import Flask, render_template, request, redirect, url_for

# Importando a bibliteca do mysql
import mysql.connector

# Cria a aplicação Flask
app = Flask(__name__)

# Configurando a conexão do banco de dados MySQL
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="senai",
        port=3306,
        database="bdteste"
    )


# ---------------------------------------------------
# Página inicial (rota "/")
# ---------------------------------------------------
@app.route('/')
def index():
    # Renderiza o arquivo "index.html" dentro da pasta templates
    return render_template("index.html")

# ---------------------------------------------------
# Rota para listar todos os clientes
# ---------------------------------------------------
@app.route('/clientes')
def listar_clientes():
    # Abre conexão com o banco
    conn = get_connection()
    # Cria cursor para executar comandos SQL
    cursor = conn.cursor(dictionary=True)  # dictionary=True faz o retorno ser em dicionário
    # Executa comando SQL para buscar todos os clientes
    cursor.execute("SELECT * FROM tbcliente")
    # Pega todos os resultados da consulta
    clientes = cursor.fetchall()
    # Fecha a conexão
    conn.close()
    # Envia os dados para o template "clientes.html"
    return render_template("clientes.html", clientes=clientes)


# ---------------------------------------------------
# Rota para Cadastrar um novo cliente
# ---------------------------------------------------
@app.route('/cadastrar-cliente',  methods=["GET", "POST"])
def cadastrar_cliente():
    # Captura os dados do formulário (a implementar)   
    if request.method == "POST":
        # Captura os dados do formulário (nome e email)
        nome            = request.form["nome"]
        rg              = request.form["rg"]
        endereco        = request.form["endereco"]
        bairro          = request.form["bairro"]
        cidade          = request.form["cidade"]
        estado          = request.form["estado"]
        telefone        = request.form["telefone"]
        email           = request.form["email"]
        data_nascimento = request.form["data_nascimento"]
        estado_civil    = request.form["estado_civil"]

        # Abre conexão com o banco
        conn = get_connection()
        cursor = conn.cursor()
      
       # Insere os dados no banco
        sql = """
                INSERT INTO tbcliente 
                 (RG, NOME, ENDERECO, BAIRRO, CIDADE, ESTADO, TELEFONE, EMAIL, DATA_NASCIMENTO, ESTADO_CIVIL)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
              """;
        valores = (rg, nome, endereco, bairro, cidade, estado, telefone, email, data_nascimento, estado_civil)

        cursor.execute(sql, valores)
        conn.commit()
        conn.close()

        # Redireciona para a lista de clientes após cadastro
        return redirect(url_for("listar_clientes"))

    return render_template("cadastro.html")

@app.route('/excluir/<int:id>')
def excluir_usuario(id):
    conexao = get_connection()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id = %s", (id,))
    conexao.commit()
    conexao.close()
    return redirect(url_for('listar_usuarios'))

# ---------------------------------------------------
# Inicia o servidor Flask se rodar o arquivo direto
# ---------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)  # debug=True atualiza automaticamente a cada alteração
