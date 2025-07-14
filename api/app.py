from flask import Flask, flash, jsonify, request, render_template, redirect, url_for, session, make_response
from database.database_config import *
from database.database_config import add_empresa
from views.api.routes import api_bp
from views.admin.routes import admin_bp
from views.user.routes import user_bp
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
#'motoristaLegal'

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'xlsx', 'csv'}
TAMANHO_PERMITIDO = 16 * 1000 * 1000

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = TAMANHO_PERMITIDO

app.register_blueprint(api_bp)

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
        dados = obter_placas()
        adminDados = obter_empresas()

        # if senha == "admin":
        #     session['logado'] = True
        #     return redirect(url_for('admin.pagina_admin'))

        if senha.upper() in dados:
            session['logado'] = True
            session['placa'] = senha.upper()
            return redirect(url_for('user.pagina_user'))
        
        elif any(
            senha.lower() == empresa.get("nome", "").lower() or
            senha.replace(".", "").replace("/", "").replace("-", "") == empresa.get("cnpj", "").replace(".", "").replace("/", "").replace("-", "")
            for empresa in adminDados
        ):
            empresa = next(e for e in adminDados if
                senha.lower() == e.get("nome", "").lower() or
                senha.replace(".", "").replace("/", "").replace("-", "") == e.get("cnpj", "").replace(".", "").replace("/", "").replace("-", "")
            )
            session['logado'] = True
            session['id_empresa'] = empresa['id']
            return redirect(url_for('admin.pagina_admin'))

        elif senha.lower() == "empresa":
            return redirect(url_for("cadastra_empresa"))

        else:
            erro = "Senha/Placa incorreta. Tente novamente."

    return render_template("login.html", erro=erro)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("exibir_login"))

@app.before_request
def verificar_autenticacao_global():
    caminhos_livres = [
        #Bem vindos
        'bem_vindo',
        
        #Login
        'exibir_login',
        
        #Template e Static
        'static',
        'cadastra_empresa',
        'lista_empresas',
        
        #API
        'api.listar_placas',
        'api.listar_dados_completos',
        'api.dados_por_placa',
        'api.listar_empresas',
        'api.distancia_semanal',
        'api.media_semanal_frota',
        'api.soma_km_semanal',  
        'api.motorista_info',
        'api.veiculo_info',
        'api.consumo_semanal_empresa'
    ]

    endpoint = request.endpoint or (request.url_rule and request.url_rule.endpoint)

    print("🔍 Endpoint acessado:", endpoint)

    if (
        endpoint in caminhos_livres
        or request.path.startswith("/static")
    ):
        return

    if not session.get("logado"):
        if request.accept_mimetypes.accept_json:
            return jsonify({"erro": "Não autenticado"}), 401
        return redirect(url_for("exibir_login"))

@app.route("/empresasCadastro", methods=["GET", "POST"])
def cadastra_empresa():
    if request.method == "POST":
        nomeEmpresa = request.form.get('nome_empresa')
        cnpjEmpresa = request.form.get('cnpj')
        
        if nomeEmpresa and cnpjEmpresa:
            add_empresa(nomeEmpresa, cnpjEmpresa)
            return redirect(url_for('exibir_login'))
        else:
            erro = "Por favor, preencha todos os campos."
            return render_template("AddEmpresas.html", erro=erro)
    
    return render_template("AddEmpresas.html")


#ROTA DE LISTA EMPRESAS
@app.route("/Listaempresas", methods=["GET", "POST"])
def lista_empresas():
    
    return render_template("listaEmpresas.html")

# Cria a pasta de uploads se não existir
if not os.path.exists('uploads'):
    os.makedirs('uploads')

# Registra os blueprints
app.register_blueprint(admin_bp)
app.register_blueprint(user_bp)

if __name__ == "__main__":
    app.run(debug=True)
