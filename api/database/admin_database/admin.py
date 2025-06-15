from database.database_config import conectar
from datetime import datetime

def obter_motoristas_completo():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            M.id AS id_motorista,
            M.nome AS nome_motorista,
            V.placa AS veiculo_placa,
            M.distancia_total,
            M.marcha_lenta_total,
            M.consumo_total,
            M.consumo_medio
        FROM Motoristas M
        LEFT JOIN Veiculos V ON M.veiculo_id = V.id
        ORDER BY M.nome
    """)

    resultados = cursor.fetchall()
    conn.close()

    for item in resultados:
        if item["marcha_lenta_total"]:
            tempo = str(item["marcha_lenta_total"])  # formato HH:MM:SS
            h, m, _ = tempo.split(":")
            item["marcha_lenta_formatada"] = f"{int(h)}h{int(m):02d}min"
        else:
            item["marcha_lenta_formatada"] = "0h00min"

    return resultados

def motorista_dados_unicos(id_empresa):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            M.data_final,
            M.data_inicial,
            M.id AS id_motorista,
            M.nome AS nome_motorista,
            M.distancia_total,
            TIME_FORMAT(M.marcha_lenta_total, '%%H:%%i:%%s') AS marcha_lenta_total,
            M.consumo_total,
            M.consumo_medio,
            M.avaliacao,
            V.placa AS placa,
            V.marca,
            V.modelo,
            CONCAT(V.marca, ' ', V.modelo) AS caminhao,
            E.nome AS empresa
        FROM Motoristas M
        JOIN Veiculos V ON M.veiculo_id = V.id
        JOIN Empresas E ON V.empresa_id = E.id
        WHERE V.empresa_id = %s
    """, (id_empresa,))

    dados = cursor.fetchall()
    cursor.close()
    conn.close()
    return dados


def veiculo_dados_unicos(id_empresa):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            V.id AS id_veiculo,
            V.placa,
            V.frota,
            V.marca,
            V.modelo,
            E.nome AS empresa,

            -- Dados mais recentes de uso do veículo (último registro do motorista)
            DATE_FORMAT(MAX(M.data_final), '%%d/%%m/%%Y') AS ultima_manutencao,
            MAX(M.data_final) AS data_final,
            MAX(M.data_inicial) AS data_inicial,
            SUM(M.distancia_total) AS distancia_total,
            SUM(M.consumo_total) AS litros_consumidos

        FROM Veiculos V
        JOIN Empresas E ON V.empresa_id = E.id
        LEFT JOIN Motoristas M ON M.veiculo_id = V.id

        WHERE V.empresa_id = %s

        GROUP BY V.id
        ORDER BY V.placa
    """, (id_empresa,))

    resultados = cursor.fetchall()
    conn.close()
    return resultados




def dados_relatorios(id_empresa):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            M.id AS id_motorista,
            M.nome AS nome_motorista,
            V.placa AS placa,
            MAX(V.data_final) AS ultima_data
        FROM Motoristas M
        JOIN Veiculos V ON M.veiculo_id = V.id
        WHERE V.empresa_id = %s
        GROUP BY M.id, M.nome, V.placa
    """, (id_empresa,))

    motoristas = cursor.fetchall()
    cursor.close()
    conn.close()
    return motoristas



def dados_por_id_motorista(id_motorista):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT nome FROM Motoristas WHERE id = %s", (id_motorista,))
    motorista = cursor.fetchone()

    if not motorista:
        conn.close()
        return None

    cursor.execute("""
        SELECT 
            data_final AS data_chegada, 
            consumo_medio AS media_km_l, 
            tempo_marcha_lenta AS total_hrs
        FROM Veiculos
        WHERE id IN (
            SELECT veiculo_id FROM Motoristas WHERE id = %s
        )
        ORDER BY data_final ASC
    """, (id_motorista,))

    registros = cursor.fetchall()
    conn.close()

    if not registros:
        return None

    return [
        {
            "data_final": r["data_chegada"],
            "media_km_l": r["media_km_l"],
            "total_hrs": r["total_hrs"],
            "motorista": motorista["nome"]
        } for r in registros
    ]

def motoristas_unicos_por_empresa(id_empresa):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            M.id AS id_motorista,
            M.nome AS nome_motorista,
            V.placa
        FROM Motoristas M
        JOIN Veiculos V ON M.veiculo_id = V.id
        WHERE M.empresa_id = %s
        AND M.id = (
            SELECT MIN(M2.id)
            FROM Motoristas M2
            WHERE M2.nome = M.nome AND M2.empresa_id = M.empresa_id
        )
        ORDER BY M.nome
    """, (id_empresa,))

    motoristas = cursor.fetchall()
    cursor.close()
    conn.close()
    return motoristas

