from flask import Flask, jsonify, request, render_template, redirect
from database.database_handler import obter_dados

app = Flask(__name__)

# ✅ Colunas padrão para os dados
COLUNAS_DADOS = [
    "motorista", "placa", "frota", "marca",
    "data", "datasSaida", "dataChegada", "qtdDias", "totalHrs",
    "KmSaida", "KmChegada", "KmRodado",
    "LtArla", "LtDiesel", "LtPorDia"
]

# ✅ Função utilitária para converter dados
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

# ================= PÁGINAS HTML ====================
@app.route("/login", methods=["GET", 'POST'])
def exibir_login():
    return render_template('loginAdmin.html')

@app.route("/autenticar", methods=["POST"])
def autenticar():
    senha = request.form.get("InputSenha")
    if senha == "admin":
        return redirect("/admin")
    return redirect('/login')

@app.route("/admin", methods=["GET", 'POST'])
def pagina_admin():
    return render_template('HomeAdmin.html')

@app.route('/admin/inserirDados', methods=['GET', "POST"])
def pagina_inserir_dados():
    return render_template('inserirExcel.html')

# ================= MAIN ====================
if __name__ == "__main__":
    app.run(debug=True)
