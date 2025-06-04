# api/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify, make_response
from database.database_util import obter_dados, obter_placas, obter_empresas, obter_relatorio_motoristas
from database.admin_database.admin import conectar, adicionar_motorista_banco, motorista_dados_unicos, veiculo_dados_unicos, motorista_dados_unicos_editar, adicionar_veiculo_banco, adicionar_motorista_banco, dados_relatorios 
import sqlite3
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
    dados = transformar_dados(obter_dados())
    filtrados = [linha for linha in dados if linha["placa"].upper() == placa.upper()]
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

@api_bp.route("/historico_viagens/<int:id_motorista>", methods=["GET"])
def historico_viagens(id_motorista):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            data_saida, origem, destino, km_rodado, consumo_diesel, consumo_arla
        FROM DadosTelemetria
        WHERE id_motorista = ?
        ORDER BY data_saida DESC
    """, (id_motorista,))
    viagens = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(viagens), 200


@api_bp.route("/media_km_frota/<int:id_empresa>", methods=["GET"])
def media_km_frota(id_empresa):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            v.frota,
            ROUND(AVG(dt.km_rodado), 1) AS media_km
        FROM Veiculos v
        JOIN DadosTelemetria dt ON v.id_veiculo = dt.id_veiculo
        WHERE dt.id_empresa = ?
        GROUP BY v.frota
    """, (id_empresa,))
    frota_media = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(frota_media), 200


@api_bp.route("/media_km_motoristas/<int:id_empresa>", methods=["GET"])
def media_km_motoristas(id_empresa):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            m.nome,
            ROUND(AVG(dt.km_rodado), 1) AS media_km
        FROM Motoristas m
        JOIN DadosTelemetria dt ON m.id_motorista = dt.id_motorista
        WHERE dt.id_empresa = ?
        GROUP BY m.nome
    """, (id_empresa,))
    media_motoristas = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(media_motoristas), 200
