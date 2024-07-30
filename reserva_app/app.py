from flask import Flask, render_template, redirect, url_for, request
import uuid
import csv

app = Flask(__name__, template_folder='templates')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/redirect")
def redirect_to_reserva():
    return redirect(url_for("reservar"))

@app.route("/reservasredirect")
def reservasredirect():
    return redirect(url_for("reservar_sala"))

@app.route("/redirectListar")
def redirectListar():
    return redirect(url_for("lista_salas"))

@app.route("/redirectCadastrar")
def redirectCadastrar():
    return redirect(url_for("cadastrar_salas"))

def cadastrar_sala(s):
    sala_id = str(uuid.uuid4())
    linha = [sala_id, s['tipo'], s['capacidade'], s['descricao'], "Sim"]
    with open("salas.csv", "a", newline='') as csvfile:
        spamwriter = csv.writer(csvfile)
        spamwriter.writerow(linha)

def carregar_salas():
    salas = []
    try:
        with open("salas.csv", "r") as csvfile:
            reader = csv.reader(csvfile)
            for linha in reader:
                sala_id, tipo, capacidade, descricao, ativa = linha
                sala = {
                    "id": sala_id,
                    "tipo": tipo,
                    "capacidade": capacidade,
                    "descricao": descricao,
                    "ativa": ativa
                }
                salas.append(sala)
    except FileNotFoundError:
        pass
    return salas

@app.route("/cadastrar_salas", methods=["GET", "POST"])
def cadastrar_salas_view():
    if request.method == "POST":
        tipo = request.form.get("tipo")
        capacidade = request.form.get("capacidade")
        descricao = request.form.get("descricao")
        cadastrar_sala({"tipo": tipo, "capacidade": capacidade, "descricao": descricao})
        return redirect(url_for("lista_salas"))
    return render_template("cadastrar-sala.html")

@app.route("/lista_salas")
def lista_salas():
    salas = carregar_salas()
    return render_template("listar-salas.html", salas=salas)

@app.route("/excluir-sala/<sala_id>", methods=["POST"])
def excluir_sala(sala_id):
    salas = carregar_salas()
    salas = [sala for sala in salas if sala["id"] != sala_id]
    
    with open("salas.csv", "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        for sala in salas:
            writer.writerow([sala['id'], sala['tipo'], sala['capacidade'], sala['descricao'], sala['ativa']])
    
    return redirect(url_for("lista_salas"))

@app.route("/desativar-sala/<sala_id>", methods=["POST"])
def desativar_sala(sala_id):
    salas = carregar_salas()
    for sala in salas:
        if sala["id"] == sala_id:
            sala["ativa"] = "Não" if sala["ativa"] == "Sim" else "Sim"
    
    with open("salas.csv", "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        for sala in salas:
            writer.writerow([sala['id'], sala['tipo'], sala['capacidade'], sala['descricao'], sala['ativa']])
    
    return redirect(url_for("lista_salas"))

@app.route("/reservas")
def reservas():
    return render_template("reservas.html")

@app.route("/detalhe-reserva")
def detalhe_reserva():
    return render_template("detalhe_reserva.html")

@app.route("/reservar_sala")
def reservar_sala():
    return render_template("reservar-sala.html")

def cadastrar_usuario(u):
    linha = [u['nome'], u['email'], u['password']]
    with open("usuarios.csv", "a", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(linha)

def validar_usuario(email, password):
    try:
        with open("usuarios.csv", "r") as csvfile:
            reader = csv.reader(csvfile)
            for linha in reader:
                nome, user_email, user_password = linha
                if email == user_email and password == user_password:
                    return True
    except FileNotFoundError:
        pass
    return False

if __name__ == '__main__':
    app.run(debug=True, port=5222)