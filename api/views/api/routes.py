# api/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify, make_response
from database.database_config import *
from database.admin_database.admin import conectar, motorista_dados_unicos, veiculo_dados_unicos, motorista_dados_unicos_editar, dados_relatorios 
from datetime import datetime
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
    return jsonify({"placas": placas}), 200

@api_bp.route("/dados")
def listar_dados_completos():
    dados = obter_dados()
    return jsonify(transformar_dados(dados))

@api_bp.route("/dados/<placa>")
def dados_por_placa(placa):
    dados = obter_dados_por_placa(placa=placa)
    filtrados = [
        linha for linha in dados
        if linha.get("placa", "").upper() == placa.upper()
    ]
    return jsonify(filtrados)

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
        conn = conectar()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT 
                WEEK(data_inicial) AS semana,
                YEAR(data_inicial) AS ano,
                SUM(distancia_viagem) AS total_km
            FROM Veiculos
            WHERE empresa_id = %s AND data_inicial IS NOT NULL
            GROUP BY ano, semana
            ORDER BY ano, semana
        """, (empresa_id,))
        
        dados = cursor.fetchall()

        if not dados:
            return jsonify({"mensagem": "Nenhum dado encontrado para essa empresa"}), 404
        
        return jsonify(dados), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 500

    finally:
        if conn:
            conn.close()

@api_bp.route("/media_semanal_frota/<int:empresa_id>", methods=["GET"], endpoint='media_semanal_frota')
def media_semanal_frota(empresa_id):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            nome AS frota,
            WEEK(data_inicial) AS semana,
            YEAR(data_inicial) AS ano,
            ROUND(AVG(distancia_viagem), 2) AS media_km
        FROM Veiculos
        WHERE empresa_id = %s
        GROUP BY nome, ano, semana
        ORDER BY nome, ano, semana
    """, (empresa_id,))
    
    dados = cursor.fetchall()
    conn.close()
    return jsonify(dados), 200


@api_bp.route("/soma_km_semanal/<int:empresa_id>", methods=["GET"], endpoint='soma_km_semanal')
def soma_km_semanal(empresa_id):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            MONTH(data_inicial) AS mes,
            YEAR(data_inicial) AS ano,
            WEEK(data_inicial) AS semana,
            SUM(distancia_viagem) AS total_km
        FROM Veiculos
        WHERE empresa_id = %s
        GROUP BY ano, mes, semana
        ORDER BY ano, mes, semana
    """, (empresa_id,))
    
    dados = cursor.fetchall()
    conn.close()
    return jsonify(dados), 200

@api_bp.route("/motorista_info/<int:motorista_id>", methods=["GET"], endpoint='motorista_info')
def motorista_info(motorista_id):
    print("motorista_id recebido:", motorista_id)
    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            m.id,
            m.nome,
            m.distancia_total,
            TIME_FORMAT(m.marcha_lenta_total, '%%H:%%i:%%s') AS marcha_lenta_total,
            m.consumo_total,
            m.consumo_medio,
            v.nome AS veiculo
        FROM Motoristas m
        LEFT JOIN Veiculos v ON m.veiculo_id = v.id
        WHERE m.id = %s
    """, (motorista_id,))

    
    dados = cursor.fetchone()
    conn.close()
    return jsonify(dados), 200

@api_bp.route("/veiculo_info/<int:veiculo_id>", methods=["GET"], endpoint='veiculo_info')
def veiculo_info(veiculo_id):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            v.id,
            v.nome,
            v.data_inicial,
            v.data_final,
            v.distancia_viagem,
            v.velocidade_maxima,
            v.velocidade_media,
            v.litros_consumidos,
            v.consumo_medio,
            TIME_FORMAT(v.tempo_marcha_lenta, '%%H:%%i:%%s') AS tempo_marcha_lenta,
            e.nome AS empresa
        FROM Veiculos v
        LEFT JOIN Empresas e ON v.empresa_id = e.id
        WHERE v.id = %s
    """, (veiculo_id,))
    
    dados = cursor.fetchone()
    conn.close()
    return jsonify(dados), 200


# NÃO TESTADA:

@api_bp.route("/consumo_semanal_diesel/<int:motorista_id>/<int:ano>/<int:mes>")
def consumo_semanal_diesel(motorista_id, ano, mes):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            WEEK(data, 1) AS semana_do_ano,
            SUM(consumo_diesel) AS total_diesel
        FROM DadosTelemetria
        WHERE motorista_id = %s
          AND YEAR(data) = %s
          AND MONTH(data) = %s
        GROUP BY WEEK(data, 1)
        ORDER BY semana_do_ano
    """, (motorista_id, ano, mes))

    resultados = cursor.fetchall()
    conn.close()
    return jsonify(resultados), 200