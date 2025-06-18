from database.database_config import conectar

# Função para coleta todos os dados do User (Utilizados):
def user_dados(placa):
    with conectar() as conn:
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT 
                M.nome,
                M.id,
                M.distancia_total,
                M.consumo_total,
                M.consumo_medio,
                M.avaliacao,
                V.placa,
                V.frota,
                V.marca,
                V.modelo,
                V.empresa_id,
                CONCAT(V.modelo, ' / ', V.marca) AS caminhao,
                MC.meta_km_por_litro
            FROM Motoristas M
            LEFT JOIN Veiculos V ON M.veiculo_id = V.id
            LEFT JOIN MetasConsumo MC 
                ON V.empresa_id = MC.empresa_id 
               AND V.marca = MC.marca 
               AND V.modelo = MC.modelo
            WHERE V.placa LIKE %s
            ORDER BY M.data_final DESC
            LIMIT 1
        """, (f"%{placa.upper()}%",))

        resultado = cursor.fetchone()

        if resultado:
            return {
                "motorista": resultado["nome"],
                "idMotorista": resultado["id"],
                "distancia_total": f"{resultado['distancia_total']} Km",
                "consumo_total": f"{resultado['consumo_total']} L",
                "consumo_medio": f"{resultado['consumo_medio']}",
                "avaliacao": f"{resultado['avaliacao']}",
                "placa": resultado["placa"],
                "frota": resultado["frota"],
                "caminhao": resultado["caminhao"],
                "meta_consumo": f"{resultado['meta_km_por_litro']}" if resultado["meta_km_por_litro"] is not None else "N/A"
            }
        else:
            return None

def historico_motorista(placa):
    with conectar() as conn:
        cursor = conn.cursor(dictionary=True)

        # Buscar o nome do motorista mais recente (baseado na maior data_final) que usou o veículo com essa placa
        cursor.execute("""
            SELECT M.nome
            FROM Motoristas M
            JOIN Veiculos V ON M.veiculo_id = V.id
            WHERE V.placa LIKE %s
            ORDER BY M.data_final DESC
            LIMIT 1
        """, (f"%{placa.upper()}%",))
        
        resultado = cursor.fetchone()
        if not resultado:
            return []

        nome_motorista = resultado["nome"]

        # Agora buscar todo o histórico desse motorista
        cursor.execute("""
            SELECT 
                M.data_inicial,
                M.data_final,
                M.consumo_medio,
                M.avaliacao
            FROM Motoristas M
            WHERE M.nome = %s
            ORDER BY M.data_final DESC
        """, (nome_motorista,))

        return cursor.fetchall()


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

