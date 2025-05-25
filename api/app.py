import os
from flask import Flask, flash, jsonify, request, render_template, redirect, url_for, session
from database.database_handler import obter_dados, placas_dados, motorista_dados, veiculo_dados, user_dados, dados_relatorios
# from excel_importer import excel_json

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
    dados = transformar_dados(obter_dados())
    placas = list({linha["placa"].upper() for linha in dados})
    return jsonify({"placas": placas})

@app.route("/api/dados", methods=["GET"])
def listar_dados_completos():
    dados = obter_dados()
    return jsonify(transformar_dados(dados))

@app.route("/api/dados/<placa>", methods=["GET"])
def dados_por_placa(placa):
    dados = transformar_dados(obter_dados())  # Já vira lista de dicts
    filtrados = [linha for linha in dados if linha["placa"].upper() == placa.upper()]
    return jsonify(filtrados)


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
        
        # Verifica se a placa existe nos dados
        dados = placas_dados()
        
        if senha == "admin":
            session.permanent = False
            session['logado'] = True
            return redirect(url_for('pagina_admin'))

        elif senha.upper() in dados:
            session.permanent = False
            session['logado'] = True
            session['placa'] = senha
            return redirect(url_for('pagina_user'))

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
    motoristas = motorista_dados()
    return render_template('motoristasAdmin.html', motoristas=motoristas)

@app.route("/admin/gestaoVeiculos", methods=["GET", "POST"])
def pagina_gestao_veiculos():
    veiculos = veiculo_dados()
    return render_template("veiculosAdmin.html", veiculos=veiculos)

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
    motoristas = dados_relatorios()
    
    return render_template("relatorioAdmin.html", motoristas=motoristas)

@app.route("/admin/logs", methods=["GET", "POST"])
def pagina_logs():
    return render_template("logsAdmin.html")


# ================= USER ====================
@app.route("/user", methods=["GET"])
def pagina_user():
    placa = session.get("placa")
    if not placa:
        return redirect(url_for("exibir_login"))

    dados = user_dados(placa)

    for linha in dados:
        try:
            km = float(linha["km_rodado"])
            horas = float(linha["total_hrs"])
            diesel = float(linha["lt_diesel"])
            arla = float(linha["lt_arla"])

            linha["velocidade_media"] = round(km / horas, 2) if horas > 0 else 0
            linha["consumo_diesel"] = round((diesel / km) * 100, 2) if km > 0 else 0
            linha["consumo_arla"] = round((arla / km) * 100, 2) if km > 0 else 0
        except (ValueError, TypeError):
            linha["velocidade_media"] = 0
            linha["consumo_diesel"] = 0
            linha["consumo_arla"] = 0

    return render_template("HomeUser.html", dados=dados[-1] if dados else {})

@app.route("/user/perfil", methods=["GET"])
def pagina_perfil():
    placa = session.get("placa")
    if not placa:
        return redirect(url_for("exibir_login"))

    dados = user_dados(placa)

    for linha in dados:
        try:
            km = float(linha["km_rodado"])
            horas = float(linha["total_hrs"])
            diesel = float(linha["lt_diesel"])
            arla = float(linha["lt_arla"])

            linha["velocidade_media"] = round(km / horas, 2) if horas > 0 else 0
            linha["consumo_diesel"] = round((diesel / km) * 100, 2) if km > 0 else 0
            linha["consumo_arla"] = round((arla / km) * 100, 2) if km > 0 else 0
        except (ValueError, TypeError):
            linha["velocidade_media"] = 0
            linha["consumo_diesel"] = 0
            linha["consumo_arla"] = 0
            
    return render_template('perfil.html', dados=dados)


@app.route("/user/config", methods=["GET","POST"])
def pagina_config():
    return render_template('config.html')

@app.route("/user/suporte", methods=["GET"])
def pagina_suporte():
    return render_template('suporte.html')


# ================= MAIN ====================
if __name__ == "__main__":
    app.run(debug=True)
