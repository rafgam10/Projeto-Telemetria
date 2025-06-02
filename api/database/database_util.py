import sqlite3, json
from datetime import datetime

DIR_DB = "api/database/telemetria.db"

#Função para conectar o DB:
def conectar():
    return sqlite3.connect(DIR_DB)

# Função para Obter Dados Geral do DB:
def obter_dados():
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM DadosTelemetria;
    """)
    dados = cursor.fetchall()
    conn.close()
    
    return dados

# Função para Obter Placas:
def obter_placas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT placa FROM Veiculos")
    dados_placas = cursor.fetchall()
    conn.close()
    
    return [placa[0].upper() for placa in dados_placas]


# Função para Obter Dados da Empresas:
def obter_empresas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Empresas")
    dados = cursor.fetchall()
    conn.close()
    return [{"id": linha[0], "nome": linha[1], "cnpj": linha[2]} for linha in dados]






# INSERT de dados:

# Função para inserir empresa:
def add_empresa(nome_empresa, cnpj):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Empresas (nome_empresa, cnpj)
        VALUES (?, ?)               
    """, (nome_empresa, cnpj))
    conn.commit()
    conn.close()
    return