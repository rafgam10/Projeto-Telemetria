from flask import Flask, flash, jsonify, request, render_template, redirect, url_for, session
from database.database_handler import obter_dados, placas_dados
from views.admin.routes import admin_bp
from views.user.routes import user_bp
import os

app = Flask(__name__)
app.secret_key = 'motoristaLegal'
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Colunas padrão
COLUNAS_DADOS = [...]  # mantém sua lista

def transformar_dados(dados):
    return [dict(zip(COLUNAS_DADOS, linha)) for linha in dados]

# ================= API ====================
@app.route("/api/placas")
def listar_placas():
    dados = transformar_dados(obter_dados())
    placas = list({linha["placa"].upper() for linha in dados})
    return jsonify({"placas": placas})

@app.route("/api/dados")
def listar_dados_completos():
    dados = obter_dados()
    return jsonify(transformar_dados(dados))

@app.route("/api/dados/<placa>")
def dados_por_placa(placa):
    dados = transformar_dados(obter_dados())
    filtrados = [linha for linha in dados if linha["placa"].upper() == placa.upper()]
    return jsonify(filtrados)

# ================= PÁGINAS LIVRES ====================
@app.route("/")
def bem_vindo():
    return render_template("BemVindo.html")

@app.route("/login", methods=["GET", "POST"])
def exibir_login():
    erro = None
    session['logado'] = None
    if request.method == "POST":
        senha = request.form.get("InputSenha")
        dados = placas_dados()

        if senha == "admin":
            session['logado'] = True
            return redirect(url_for('admin.pagina_admin'))

        elif senha.upper() in dados:
            session['logado'] = True
            session['placa'] = senha
            return redirect(url_for('user.pagina_user'))

        else:
            erro = "Senha/Placa incorreta. Tente novamente."

    return render_template("login.html", erro=erro)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("exibir_login"))

@app.before_request
def verificar_autenticacao_global():
    caminhos_livres = ['exibir_login', 'listar_placas', 'listar_dados_completos', 'dados_por_placa', 'static']
    endpoint = request.endpoint
    if (
        endpoint in caminhos_livres
        or (endpoint and endpoint.startswith("api"))
        or request.path.startswith("/static")
    ):
        return

    if not session.get("logado"):
        return redirect(url_for("exibir_login"))

# Cria a pasta de uploads se não existir
if not os.path.exists('uploads'):
    os.makedirs('uploads')

# Registra os blueprints
app.register_blueprint(admin_bp)
app.register_blueprint(user_bp)

if __name__ == "__main__":
    app.run(debug=True)
