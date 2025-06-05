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
    
    cursor.execute("SELECT * FROM DadosTelemetria;")
    dados = cursor.fetchall()
    print(">>> DADOS BRUTOS:", dados)
    
    conn.close()
    return dados

# Função para Obter Dados por placa do DB:

def transformar_dados(cursor, dados):
    colunas = [desc[0] for desc in cursor.description]
    resultado = []
    for linha in dados:
        dicionario = dict(zip(colunas, linha))
        resultado.append(dicionario)
    return resultado

def obter_dados_por_placa(placa):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT DadosTelemetria.*, Veiculos.placa
        FROM DadosTelemetria
        JOIN Veiculos ON DadosTelemetria.id_veiculo = Veiculos.id_veiculo
        WHERE Veiculos.placa = ?;
    """, (placa.upper(),))

    dados = cursor.fetchall()
    resultado = transformar_dados(cursor, dados)

    conn.close()
    return resultado

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


###### Relatório #########

def obter_relatorio_motoristas(id_empresa):
    conn = conectar()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            m.id_motorista,
            m.nome,
            COUNT(dt.id_telemetria) AS total_viagens,
            ROUND(SUM(dt.km_rodado), 1) AS km_total,
            ROUND(SUM(dt.consumo_diesel), 2) AS diesel_total,
            ROUND(SUM(dt.consumo_arla), 2) AS arla_total,
            MAX(dt.data_saida) AS ultima_viagem
        FROM Motoristas m
        LEFT JOIN DadosTelemetria dt ON m.id_motorista = dt.id_motorista
        WHERE m.id_empresa = ?
        GROUP BY m.id_motorista, m.nome
        ORDER BY m.nome
    """, (id_empresa,))

    dados = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return dados



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