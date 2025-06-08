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

    cursor.execute(f"""
        SELECT
            M.id AS id_motorista,
            M.nome AS nome_motorista,
            M.distancia_total,
            TIME_FORMAT(M.marcha_lenta_total, '%H:%i:%s') AS marcha_lenta_total,
            M.consumo_total,
            M.consumo_medio
        FROM Motoristas M
        WHERE M.veiculo_id IN (
            SELECT id FROM Veiculos WHERE empresa_id = {id_empresa}
        )
    """, ())

    dados = cursor.fetchall()
    conn.close()
    return dados

def motorista_dados_unicos(id_empresa):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            M.data_final,
            M.id AS id_motorista,
            M.nome AS nome_motorista,
            M.distancia_total,
            TIME_FORMAT(M.marcha_lenta_total, '%%H:%%i:%%s') AS marcha_lenta_total,
            M.consumo_total,
            M.consumo_medio
        FROM Motoristas M
        JOIN Veiculos V ON M.veiculo_id = V.id
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
            V.frota,
            V.marca,
            V.modelo,
            V.id AS id_veiculo,
            V.placa,
            DATE_FORMAT(MAX(V.data_final), '%%d/%%m/%%Y') AS ultima_manutencao,
            V.litros_consumidos,
            V.data_final,
            V.distancia_viagem
        FROM Veiculos V
        WHERE V.empresa_id = %s
        GROUP BY V.id
        ORDER BY V.placa
    """, (id_empresa,))

    resultados = cursor.fetchall()
    conn.close()
    return resultados


def dados_relatorios():
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
        GROUP BY M.id, M.nome, V.placa
    """)

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
