# api/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify, make_response
from database.database_config import *
from database.admin_database.admin import conectar, motorista_dados_unicos, veiculo_dados_unicos, dados_relatorios 
from datetime import date, datetime, timedelta
import os

api_bp = Blueprint("api", __name__, url_prefix="/api")

# Colunas padrão
COLUNAS_DADOS = [...]  # mantém sua lista

def transformar_dados(dados):
    return [dict(zip(COLUNAS_DADOS, linha)) for linha in dados]

# ================= API ====================
@api_bp.route("/empresas")
def listar_empresas():
    empresas = obter_empresas()
    return make_response(jsonify(empresas), 200)

@api_bp.route("/placas")
def listar_placas():
    placas = obter_placas()
    return make_response(jsonify({"placas": placas}), 200)

@api_bp.route("/dados")
def listar_dados_completos():
    dados = obter_dados()
    return jsonify(transformar_dados(dados))

@api_bp.route("/dados/<placa>")
def dados_por_placa(placa):
    dados = obter_dados_por_placa(placa=placa)
    filtrados = []

    for linha in dados:
        nova_linha = linha.copy()

        # Converte timedelta para string legível
        if isinstance(nova_linha.get("tempo_marcha_lenta"), timedelta):
            nova_linha["tempo_marcha_lenta"] = str(nova_linha["tempo_marcha_lenta"])

        # Converte datas (date ou datetime) para string 'YYYY-MM-DD'
        for campo in ["data_inicial", "data_final"]:
            valor = nova_linha.get(campo)
            if isinstance(valor, (date, datetime)):
                nova_linha[campo] = valor.strftime("%d/%m/%Y")

        filtrados.append(nova_linha)

    return make_response(jsonify(filtrados), 200)

@api_bp.route("/motoristas/<int:id_empresa>", methods=["GET"])
def relatorio_motoristas(id_empresa):
    dados = obter_relatorio_motoristas(id_empresa)
    return jsonify(dados), 200

@api_bp.route("/consumo_mensal/<int:id_empresa>", methods=["GET"])
def consumo_mensal(id_empresa):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            strftime('%Y-%m', data_saida) AS mes,
            ROUND(SUM(consumo_diesel), 2) AS diesel,
            ROUND(SUM(consumo_arla), 2) AS arla
        FROM DadosTelemetria
        WHERE id_empresa = ?
        GROUP BY mes
        ORDER BY mes
    """, (id_empresa,))
    resultados = [dict(mes=row[0], diesel=row[1], arla=row[2]) for row in cursor.fetchall()]
    conn.close()
    return jsonify(resultados), 200


@api_bp.route("/media_km_motoristas/<int:id_empresa>", methods=["GET"])
def media_km_motoristas(id_empresa):
    conn = conectar()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            m.id_motorista,
            m.nome,
            v.frota,
            STRFTIME('%Y-%m', dt.data_saida) AS mes,
            ROUND(AVG(dt.km_rodado), 1) AS media_km
        FROM Motoristas m
        JOIN DadosTelemetria dt ON m.id_motorista = dt.id_motorista
        JOIN Veiculos v ON dt.id_veiculo = v.id_veiculo
        WHERE dt.id_empresa = ?
        GROUP BY m.nome, v.frota, mes
        ORDER BY mes ASC
    """, (id_empresa,))

    media_motoristas = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(media_motoristas), 200

@api_bp.route("/media_km_frota/<int:id_empresa>", methods=["GET"])
def media_km_frota(id_empresa):
    conn = conectar()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            v.frota,
            STRFTIME('%Y-%m', dt.data_saida) AS mes,
            ROUND(AVG(dt.km_rodado), 1) AS media_km
        FROM Veiculos v
        JOIN DadosTelemetria dt ON v.id_veiculo = dt.id_veiculo
        WHERE dt.id_empresa = ?
        GROUP BY v.frota, mes
        ORDER BY mes ASC
    """, (id_empresa,))

    frota_media = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(frota_media), 200

####################################
############ NOVAS ROTAS ###########
####################################
# E TESTANDA:

@api_bp.route("/distancia_semanal/<int:empresa_id>", methods=["GET"], endpoint="distancia_semanal")
def distancia_semanal(empresa_id):
    try:    
        dados = distancia_semanal_func(empresa_id)

        if not dados:
            return make_response(jsonify({"mensagem": "Nenhum dado encontrado para essa empresa"}), 404)
            
        return make_response(jsonify(dados), 200)

    except Exception as e:
        return make_response(jsonify({"erro": str(e)}), 500)


@api_bp.route("/media_semanal_frota/<int:empresa_id>", methods=["GET"], endpoint='media_semanal_frota')
def media_semanal_frota(empresa_id):
    try:
        dados = media_semanal_frota_func(empresa_id)
        
        if not dados:
            return make_response(jsonify({"mensagem": "Nenhum dado encontrado para essa empresa"}), 404)
        
        return make_response(jsonify(dados), 200)

    except Exception as e:
        return make_response(jsonify({"erro": str(e)}), 500)

@api_bp.route("/soma_km_semanal/<int:empresa_id>", methods=["GET"], endpoint='soma_km_semanal')
def soma_km_semanal(empresa_id):
    try: 
        dados = soma_km_semanal_func(empresa_id)

        if not dados:
            return make_response(jsonify({"mensagem": "Nenhum dado encontrado para essa empresa"}), 404)

        return make_response(jsonify(dados), 200)
    
    except Exception as e:
        return make_response(jsonify({"erro": str(e)}), 500)

@api_bp.route("/motorista_info/<int:motorista_id>", methods=["GET"], endpoint='motorista_info')
def motorista_info(motorista_id):
    try:
        dados = motorista_info_func(motorista_id)

        if not dados:
            return make_response(jsonify({"mensagem": "Nenhum dado encontrado para essa empresa"}), 404)

        return make_response(jsonify(dados), 200)
    
    except Exception as e:
        return make_response(jsonify({"erro": str(e)}), 500)

@api_bp.route("/veiculo_info/<int:veiculo_id>", methods=["GET"], endpoint='veiculo_info')
def veiculo_info(veiculo_id):
    try:
        dados = veiculo_info_func(veiculo_id)

        if not dados:
                return make_response(jsonify({"mensagem": "Nenhum dado encontrado para essa empresa"}), 404)

        return make_response(jsonify(dados), 200)
    
    except Exception as e:
        return make_response(jsonify({"erro": str(e)}), 500)

@api_bp.route("/consumo_semanal_empresa/<int:id_empresa>")
def consumo_semanal_empresa(id_empresa):

    try:
        dados = consumo_semanal_empresa_func(id_empresa)
        dados.reverse()  # ordem cronológica (da mais antiga para a mais recente)

        for item in dados:
            data_i = item['data_inicial'].strftime('%d/%m/%Y')
            data_f = item['data_final'].strftime('%d/%m/%Y')
            item['semana'] = f"{data_i} - {data_f}"
            del item['data_inicial']
            del item['data_final']

        if not dados:
                return make_response(jsonify({"mensagem": "Nenhum dado encontrado para essa empresa"}), 404)

        return make_response(jsonify(dados), 200)

    except Exception as e:
        print(f"Erro ao buscar consumo semanal: {str(e)}")
        return make_response(jsonify([]), 404)

