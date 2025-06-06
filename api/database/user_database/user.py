from database.database_config import conectar

def user_dados(placa_ou_frota):
    conn = conectar()
    cursor = conn.cursor()

    # Faz busca com LIKE para combinar parte do nome
    cursor.execute("""
        SELECT 
            M.nome AS nome_motorista,
            V.nome AS frota_placa,
            ROUND(V.velocidade_media, 2),
            V.velocidade_maxima,
            ROUND(V.consumo_medio, 2),
            V.litros_consumidos,
            V.distancia_viagem,
            SEC_TO_TIME(TIME_TO_SEC(V.tempo_marcha_lenta)) AS tempo_marcha_lenta
        FROM Veiculos V
        LEFT JOIN Motoristas M ON M.veiculo_id = V.id
        WHERE V.nome LIKE %s
        LIMIT 1
    """, (f"%{placa_ou_frota.upper()}%",))

    resultado = cursor.fetchone()
    conn.close()

    if resultado:
        tempo_marcha = resultado[7]
        h, m, _ = str(tempo_marcha).split(":")
        return {
            "motorista": resultado[0],
            "frota": resultado[1],
            "velocidade_media": f"{resultado[2]} Km/h",
            "velocidade_maxima": f"{resultado[3]} Km/h",
            "consumo_medio": f"{resultado[4]} L/100Km",
            "litros_consumidos": f"{resultado[5]} L",
            "distancia_viagem": f"{resultado[6]} Km",
            "marcha_lenta": f"{int(h)}h{int(m):02d}min"
        }
    else:
        return None


def historico_user(placa_ou_frota):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            DATE_FORMAT(data_inicial, '%%d/%%m/%%Y') AS data_inicial,
            DATE_FORMAT(data_final, '%%d/%%m/%%Y') AS data_final,
            ROUND(distancia_viagem, 2) AS distancia_viagem,
            ROUND(consumo_medio, 2) AS consumo_medio,
            ROUND(litros_consumidos, 2) AS litros_consumidos
        FROM Veiculos
        WHERE nome LIKE %s
    """, (f"%{placa_ou_frota.upper()}%",))

    resultados = cursor.fetchall()
    conn.close()
    return resultados

