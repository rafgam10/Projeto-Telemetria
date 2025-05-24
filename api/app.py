import os
from flask import Flask, flash, jsonify, request, render_template, redirect, url_for, session
from database.database_handler import obter_dados
from excel_importer import excel_json

app = Flask(__name__)
app.secret_key = 'motoristaLegal'
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Colunas padrão para os dados
COLUNAS_DADOS = [
    "motorista", "nr_acerto",
    "data", "data_saida", "data_chegada",
    "km_saida", "km_chegada", "km_rodado", "km_vazio", "porcento_vazio",
    "qtd_dias", "total_hrs",
    "frota", "placa", "marca_modelo", "ano_veiculo",
    "lt_diesel", "media", "lt_arla", "porcento_arla",
    "nr_equipamento", "marca_modelo_equipamento", "ano_equipamento",
    "lt_diesel_equip", "media_1", "media_2",
    "lt_por_dia", "km_rodado_dup", "dif", "media_dup", "dif_media"
]

# Utilitário para transformar dados brutos em dicionários
def transformar_dados(dados):
    return [dict(zip(COLUNAS_DADOS, linha)) for linha in dados]

# ================= API ====================
@app.route("/api/placas", methods=["GET"]) 
def listar_placas():
    dados = obter_dados()
    placas = list({linha[1].upper() for linha in dados})
    return jsonify({"placas": placas})

@app.route("/api/dados", methods=["GET"])
def listar_dados_completos():
    dados = obter_dados()
    return jsonify(transformar_dados(dados))

@app.route("/api/dados/<placa>", methods=["GET"])
def dados_por_placa(placa):
    dados = obter_dados()
    filtrados = [linha for linha in dados if linha[1].upper() == placa.upper()]
    return jsonify(transformar_dados(filtrados))


# ================ BEM VINDO ==================
@app.route("/", methods=["GET"])
def bem_vindo():
    return render_template('BemVindo.html')

# ================= LOGIN ====================
@app.route("/login", methods=["GET", "POST"])
def exibir_login():
    erro = None
    session['logado'] = None
    if request.method == "POST":
        senha = request.form.get("InputSenha")
        if senha == "admin":
            session.permanent = False  # Sessão acaba ao fechar o navegador
            session['logado'] = True
            return redirect(url_for('pagina_admin'))
        else:
            erro = "Senha/Placa incorreta. Tente novamente."
    return render_template('login.html', erro=erro)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('exibir_login'))

# ================= PROTEÇÃO DE ROTAS ====================
@app.before_request
def verificar_autenticacao_global():
    caminhos_livres = ['exibir_login', 'autenticar', 'static', 'listar_placas', 'listar_dados_completos', 'dados_por_placa' ]
    endpoint = request.endpoint

    if (
        endpoint in caminhos_livres
        or (endpoint and endpoint.startswith('api'))
        or request.path.startswith('/static')
    ):
        return

    if not session.get('logado'):
        return redirect(url_for('exibir_login'))


# ================= ADMIN ====================
@app.route("/admin", methods=["GET", 'POST'])
def pagina_admin():
    return render_template('HomeAdmin.html')

@app.route("/admin/gestaoMotoristas", methods=["GET", "POST"])
def pagina_gestao_motoristas():
    
    
    
    return render_template('motoristasAdmin.html')

@app.route("/admin/gestaoVeiculos", methods=["GET", "POST"])
def pagina_gestao_veiculos():
    return render_template("veiculosAdmin.html")

# ==== Upload do Arquivo Excel ========

if not os.path.exists('uploads'):
    os.makedirs('uploads')

@app.route('/admin/inserirDados', methods=['GET', "POST"])
def pagina_inserir_dados():
    return render_template('importAdmin.html')


@app.route('/admin/importar-excel', methods=["POST"])
def importar_Excel():
    # Verifica se o arquivo foi enviado
    if 'arquivo_excel' not in request.files:
        flash('Nenhum arquivo enviado', 'error')
        return redirect(url_for('pagina_inserir_dados'))
    
    arquivo = request.files['arquivo_excel']
    
    # Verifica se o arquivo tem um nome
    if arquivo.filename == '':
        flash('Nenhum arquivo selecionado', 'error')
        return redirect(url_for('pagina_inserir_dados'))
    
    # Verifica se é um arquivo Excel (opcional)
    if not arquivo.filename.lower().endswith(('.xls', '.xlsx', '.xlsm')):
        flash('Formato de arquivo inválido. Envie um arquivo Excel.', 'error')
        return redirect(url_for('pagina_inserir_dados'))
    
    try:
        # Salva o arquivo na pasta uploads
        caminho = os.path.join("uploads", arquivo.filename)
        arquivo.save(caminho)
        flash('Arquivo importado com sucesso!', 'success')
        return redirect(url_for('pagina_inserir_dados'))
    
    except Exception as e:
        flash(f'Erro ao importar arquivo: {str(e)}', 'error')
        return redirect(url_for('pagina_inserir_dados'))


@app.route("/admin/relatorios", methods=["GET", "POST"])
def pagina_relatorios():
    return render_template("relatorioAdmin.html")

@app.route("/admin/logs", methods=["GET", "POST"])
def pagina_logs():
    return render_template("logsAdmin.html")


# ================= USER ====================
@app.route("/user", methods=["GET"])
def pagina_user():
    return render_template('HomeUser.html')

@app.route("/user/perfil", methods=["GET"])
def pagina_perfil():
    return render_template('perfilUser.html')

@app.route("/user/historico", methods=["GET"])
def pagina_historico():
    return render_template('historicoUser.html')

@app.route("/user/config", methods=["GET"])
def pagina_config():
    return render_template('configUser.html')

@app.route("/user/suporte", methods=["GET"])
def pagina_suporte():
    return render_template('suporteUser.html')


# ================= MAIN ====================
if __name__ == "__main__":
    app.run(debug=True)
