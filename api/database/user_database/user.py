from database.database_config import conectar

# Função para coleta todos os dados do User (Utilizados):
def user_dados(placa_ou_frota):
    with conectar() as conn:
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT 
                M.nome AS nome_motorista,
                CONCAT(V.frota, ' / ', V.placa) AS frota_placa,
                ROUND(V.velocidade_media, 2) AS velocidade_media,
                V.velocidade_maxima,
                ROUND(V.consumo_medio, 2) AS consumo_medio,
                V.litros_consumidos,
                V.distancia_viagem,
                SEC_TO_TIME(TIME_TO_SEC(V.tempo_marcha_lenta)) AS tempo_marcha_lenta
            FROM Veiculos V
            LEFT JOIN Motoristas M ON M.veiculo_id = V.id
            WHERE V.placa LIKE %s OR V.frota LIKE %s
            LIMIT 1
        """, (f"%{placa_ou_frota.upper()}%", f"%{placa_ou_frota.upper()}%"))

        resultado = cursor.fetchone()

        if resultado:
            tempo_marcha = resultado["tempo_marcha_lenta"]
            h, m, _ = str(tempo_marcha).split(":")
            return {
                "motorista": resultado["nome_motorista"],
                "frota": resultado["frota_placa"],
                "velocidade_media": f"{resultado['velocidade_media']} Km/h",
                "velocidade_maxima": f"{resultado['velocidade_maxima']} Km/h",
                "consumo_medio": f"{resultado['consumo_medio']} L/100Km",
                "litros_consumidos": f"{resultado['litros_consumidos']} L",
                "distancia_viagem": f"{resultado['distancia_viagem']} Km",
                "marcha_lenta": f"{int(h)}h{int(m):02d}min"
            }
        else:
            return None 


def perfil_user(placa_ou_frota):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            DATE_FORMAT(V.data_inicial, '%%d/%%m/%%Y') AS data_inicial,
            DATE_FORMAT(V.data_final, '%%d/%%m/%%Y') AS data_final,
            ROUND(V.distancia_viagem, 2) AS distancia_viagem,
            ROUND(V.consumo_medio, 2) AS consumo_medio,
            ROUND(V.litros_consumidos, 2) AS litros_consumidos,
            ROUND(V.velocidade_media, 2) AS velocidade_media,
            V.velocidade_maxima,
            SEC_TO_TIME(TIME_TO_SEC(V.tempo_marcha_lenta)) AS tempo_marcha_lenta
        FROM Veiculos V
        WHERE V.placa LIKE %s OR V.frota LIKE %s
        ORDER BY V.data_inicial DESC
    """, (f"%{placa_ou_frota.upper()}%", f"%{placa_ou_frota.upper()}%"))

    resultados = cursor.fetchall()
    conn.close()
    return resultados

