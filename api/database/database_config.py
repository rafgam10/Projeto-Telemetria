import mysql.connector
from datetime import datetime

DIR_DB = "api/database/telemetria.db"

#Função para conectar o DB:
def conectar():
    return mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="root",
        database="DBTelemetria"
    )
    
def obter_dados():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM DadosTelemetria;")
    dados = cursor.fetchall()
    cursor.close()
    conn.close()
    return dados


def obter_motorista():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Motoristas;")
    dados = cursor.fetchall()
    cursor.close()
    conn.close()
    return dados
    
    
# Obter dados gerais da tabela Veiculos (exemplo):
def obter_veiculos():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Veiculos;")
    dados = cursor.fetchall()
    cursor.close()
    conn.close()
    return dados

# Obter dados por placa (veículo.nome representa a placa/frota):
def obter_dados_por_placa(placa):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT v.*, m.nome AS motorista_nome
        FROM Veiculos v
        LEFT JOIN Motoristas m ON m.veiculo_id = v.id
        WHERE UPPER(v.nome) = %s;
    """, (placa.upper(),))
    dados = cursor.fetchall()
    cursor.close()
    conn.close()
    return dados

# Obter todas as placas (nomes dos veículos):
def obter_placas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT nome FROM Veiculos")
    dados_placas = cursor.fetchall()
    cursor.close()
    conn.close()
    return [placa[0].upper() for placa in dados_placas]

# Obter dados das empresas:
def obter_empresas():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Empresas")
    dados = cursor.fetchall()
    cursor.close()
    conn.close()
    return dados

# Relatório de motoristas por empresa (buscando motoristas cujos veículos pertencem à empresa):
def obter_relatorio_motoristas(id_empresa):
    conn = conectar()
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
    dados = cursor.fetchall()
    cursor.close()
    conn.close()
    return dados

# Inserir empresa:
def add_empresa(nome, cnpj):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Empresas (nome, cnpj)
        VALUES (%s, %s)
    """, (nome, cnpj))
    conn.commit()
    cursor.close()
    conn.close()
    return "Empresa adicionada com sucesso"