from flask import Flask, flash, render_template, redirect, url_for, request
import uuid
import csv
import os

app = Flask(__name__, template_folder='templates')
app.secret_key = 'passwordQUalquer'
users_db = []


csv_files = ["salas.csv", "reservas.csv", "usuarios.csv"]
for file in csv_files:
    if not os.path.exists(file):
        with open(file, "w") as f:
            pass

def escrever_csv(filename, data):
    with open(filename, "a", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data)

def ler_do_csv(filename):
    data = []
    try:
        with open(filename, "r") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                data.append(row)
    except FileNotFoundError:
        pass
    return data

@app.route("/")
def index():
    return render_template("index.html")

# Rotas de redirecionamento
@app.route("/redirectEditar")
def redirectEditar():
    return redirect(url_for("editar_sala"))

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

@app.route("/redirectCadastro")
def redirectCadastro():
    return redirect(url_for("cadastro"))

# Métodos
def cadastrar_sala(s):
    sala_id = str(uuid.uuid4())
    linha = [sala_id, s['tipo'], s['capacidade'], s['descricao'], "Sim"]
    escrever_csv("salas.csv", linha)

def carregar_salas():
    salas = []
    for linha in ler_do_csv("salas.csv"):
        if linha:  
            sala = {
                "id": linha[0],
                "tipo": linha[1],
                "capacidade": linha[2],
                "descricao": linha[3],
                "ativa": linha[4]
            }
            salas.append(sala)
    return salas

def carregar_salas_ordenadas():
    salas = carregar_salas()  
    
   
    for i in range(len(salas)):
        for j in range(len(salas) - 1):
            if salas[j]['id'] > salas[j + 1]['id']:
              
                salas[j], salas[j + 1] = salas[j + 1], salas[j]
    
    return salas

def busca_binaria(salas, sala_id):
    esquerda, direita = 0, len(salas) - 1
    while esquerda <= direita:
        meio = (esquerda + direita) // 2
        sala_atual = salas[meio]
        if sala_atual['id'] == sala_id:
            return meio
        elif sala_atual['id'] < sala_id:
            esquerda = meio + 1
        else:
            direita = meio - 1
    return -1  

# Rotas e suas funções
@app.route("/cadastrar_salas", methods=["GET", "POST"])
def cadastrar_salas_view():
    if request.method == "POST":
        tipo = request.form.get("tipo")
        capacidade = request.form.get("capacidade")
        descricao = request.form.get("descricao")
        cadastrar_sala({"tipo": tipo, "capacidade": capacidade, "descricao": descricao})
        flash('Sala cadastrada com sucesso!', 'success')
        return redirect(url_for("lista_salas"))
    return render_template("cadastrar-sala.html")

@app.route("/lista_salas")
def lista_salas():
    salas = carregar_salas()
    return render_template("listar-salas.html", salas=salas)

@app.route("/editar_sala/<sala_id>", methods=["GET", "POST"])
def editar_sala(sala_id):
    salas = carregar_salas()
    sala_to_edit = next((sala for sala in salas if sala["id"] == sala_id), None)
    
    if request.method == "POST":
        sala_to_edit["tipo"] = request.form.get("tipo")
        sala_to_edit["capacidade"] = request.form.get("capacidade")
        sala_to_edit["descricao"] = request.form.get("descricao")
        
        with open("salas.csv", "w", newline='') as csvfile:
            writer = csv.writer(csvfile)
            for sala in salas:
                writer.writerow([sala['id'], sala['tipo'], sala['capacidade'], sala['descricao'], sala['ativa']])
        
        flash('Sala editada com sucesso!', 'success')
        return redirect(url_for("lista_salas"))
    
    return render_template("editar-sala.html", sala=sala_to_edit)

@app.route("/excluir-sala/<sala_id>", methods=["POST"])
def excluir_sala(sala_id):
    salas = carregar_salas_ordenadas()  
    indice = busca_binaria(salas, sala_id)  

    if indice != -1: 
        del salas[indice] 
        
        
        with open("salas.csv", "w", newline='') as csvfile:
            writer = csv.writer(csvfile)
            for sala in salas:
                writer.writerow([sala['id'], sala['tipo'], sala['capacidade'], sala['descricao'], sala['ativa']])
        
        flash('Sala excluída com sucesso!', 'success')
    else:
        flash('Sala não encontrada!', 'error')

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
    
    flash('Sala desativada com sucesso!', 'success')
    return redirect(url_for("lista_salas"))

@app.route("/reservas")
def reservas():
    return render_template("reservas.html")

@app.route("/detalhe-reserva")
def detalhe_reserva():
    return render_template("detalhe_reserva.html")

def cadastrar_reserva(reserva):
    csv_file_path = 'reservas.csv'
    file_exists = os.path.isfile(csv_file_path)
    
    with open(csv_file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['sala_id', 'inicio'])
        writer.writerow([reserva['sala_id'], reserva['start_time']])

@app.route("/reservar_sala", methods=["GET", "POST"])
def reservar_sala():
    if request.method == "POST":
        sala_id = request.form.get("sala")
        start_time = request.form.get("inicio")
        
        cadastrar_reserva({
            "sala_id": sala_id,
            "start_time": start_time,
        })
        
        flash('Reserva realizada com sucesso!', 'success')
    
    return render_template("reservar-sala.html")

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        password = request.form['password']
  
        users_db.append({'nome': nome, 'email': email, 'password': password})
        cadastrar_usuario({'nome': nome, 'email': email, 'password': password})
        
        flash('Cadastro realizado com sucesso!', 'success')
        return redirect(url_for('index'))
    
    return render_template('cadastro.html')

def cadastrar_usuario(u):
    escrever_csv("usuarios.csv", [u['nome'], u['email'], u['password']])

if __name__ == '__main__':
    app.run(debug=True, port=5112)