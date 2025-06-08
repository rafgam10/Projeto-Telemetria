import mysql.connector
from datetime import datetime

DIR_DB = "api/database/telemetria.db"

# Função para conectar ao banco
def conectar():
    return mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="root",
        database="DBTelemetria"
    )

# Obter todos os dados da tabela DadosTelemetria
def obter_dados():
    with conectar() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM DadosTelemetria;")
        return cursor.fetchall()

# Obter todos os motoristas
def obter_motoristas():
    with conectar() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Motoristas;")
        return cursor.fetchall()

# Obter todos os veículos
def obter_veiculos():
    with conectar() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Veiculos;")
        return cursor.fetchall()

# Obter dados de veículo por placa
def obter_dados_por_placa(placa):
    with conectar() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT v.*, m.nome AS motorista_nome
            FROM Veiculos v
            LEFT JOIN Motoristas m ON m.veiculo_id = v.id
            WHERE UPPER(v.placa) = %s;
        """, (placa.upper(),))
        return cursor.fetchall()

# Obter todas as placas de veículos
def obter_placas():
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT placa FROM Veiculos;")
        return [placa[0].upper() for placa in cursor.fetchall()]

# Obter empresas
def obter_empresas():
    with conectar() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Empresas;")
        return cursor.fetchall()

# Obter metas de consumo
def obter_metas_consumo():
    with conectar() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM MetasConsumo;")
        return cursor.fetchall()

# Obter relatório de motoristas por empresa
def obter_relatorio_motoristas(id_empresa):
    with conectar() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                m.id AS id_motorista,
                m.nome,
                COUNT(v.id) AS total_veiculos,
                COALESCE(SUM(m.distancia_total), 0) AS distancia_total,
                m.marcha_lenta_total,
                COALESCE(SUM(m.consumo_total), 0) AS consumo_total,
                COALESCE(AVG(m.consumo_medio), 0) AS consumo_medio
            FROM Motoristas m
            JOIN Veiculos v ON m.veiculo_id = v.id
            WHERE v.empresa_id = %s
            GROUP BY m.id, m.nome, m.marcha_lenta_total
            ORDER BY m.nome;
        """, (id_empresa,))
        return cursor.fetchall()

# Inserir uma nova empresa
def add_empresa(nome, cnpj):
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Empresas (nome, cnpj)
            VALUES (%s, %s)
        """, (nome, cnpj))
        conn.commit()
    return "Empresa adicionada com sucesso"
