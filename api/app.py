from flask import Flask, jsonify, request, render_template, redirect
from flask_restful import Api, Resource
from models.motorista import MotoristaModel

from database.database_handler import obter_dados

app = Flask(__name__)

#Rota da API:
@app.route("/api/placas", methods=["GET"]) 
def listar_placas():
    dados = obter_dados()
    placas = list({linha[1] for linha in dados})
    return jsonify({"placas":placas})

@app.route("/api/dados", methods=["GET"])
def listar_dados_completos():
    dados = obter_dados()
    colunas = [
        "motorista", "placa", "frota", "marca",
        "data", "datasSaida", "dataChegada", "qtdDias", "totalHrs",
        "KmSaida", "KmChegada", "KmRodado",
        "LtArla", "LtDiesel", "LtPorDia"
        ]
    resultado = [dict(zip(colunas, linha)) for linha in dados]
    return jsonify(resultado)

@app.route("/api/dados/<placa>", methods=["GET"])
def dados_por_placa(placa):
    dados = obter_dados()
    colunas = [
        "motorista", "placa", "frota", "marca",
        "data", "datasSaida", "dataChegada", "qtdDias", "totalHrs",
        "KmSaida", "KmChegada", "KmRodado",
        "LtArla", "LtDiesel", "LtPorDia"
    ]
    filtrados = [dict(zip(colunas, linha)) for linha in dados if linha[1] == placa.upper()]
    return jsonify(filtrados)


# Rota para página Login:
@app.route("/login", methods=['POST',])
def IndexLogin():
    return render_template('loginAdmin.html')

# Rota para autenticação do Login:
@app.route("/autenticar", methods=["POST",])
def autenticar():
    pass

# Rotas para páginas Admin
@app.route("/admin", methods=["GET"])
def IndexAdmin():
    return render_template('HomeAdmin.html')

@app.route('/admin/inserirDados', methods=["POST"])
def Index_Inserir_Dados():
    return render_template('inserirExcel.html')


# Compilador: 
if __name__ == "__main__":
    app.run(debug=True)
