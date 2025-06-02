import sqlite3, json
from database.database_util import conectar

# Funções para User:

def user_dados(placa):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            M.nome AS nome_motorista,
            V.placa,
            V.frota,
            V.marca || ' / ' || V.modelo AS caminhao_modelo_marca,
            ROUND(AVG(D.velocidade_media), 2),
            MAX(D.rotacao_maxima),
            ROUND(AVG(D.consumo_diesel), 1),
            ROUND(AVG(D.consumo_arla), 1),
            ROUND(SUM(D.km_rodado),2),
            SUM(CAST(SUBSTR(D.marcha_lenta, 1, INSTR(D.marcha_lenta, 'h') - 1) AS INTEGER)) * 60 +
            SUM(CAST(SUBSTR(D.marcha_lenta, INSTR(D.marcha_lenta, 'h') + 1, -1) AS INTEGER)) as total_minutos_marcha_lenta
        FROM DadosTelemetria D
        JOIN Motoristas M ON D.id_motorista = M.id_motorista
        JOIN Veiculos V ON D.id_veiculo = V.id_veiculo
        WHERE V.placa = ?
        GROUP BY D.id_motorista, D.id_veiculo;
    """, (placa.upper(),))
    
    resultado = cursor.fetchone()
    conn.close()
    
    if resultado:
        # Convertendo minutos de marcha lenta para "XhYmin"
        total_min = resultado[-1]
        horas = total_min // 60
        minutos = total_min % 60

        return {
            "motorista": resultado[0],
            "placa": resultado[1],
            "frota": resultado[2],
            "modelo": resultado[3],
            "velocidade_media": f"{resultado[4]} Km/h",
            "rotacao_maxima": f"{resultado[5]} RPM",
            "consumo_diesel": f"{resultado[6]} L/100Km",
            "consumo_arla": f"{resultado[7]} L/100Km",
            "km_rodado": f"{resultado[8]} Km",
            "marcha_lenta": f"{horas}h{minutos:02d}min"
        }
    else:
        return None
    
def historico_user(placa):
    conn = conectar()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            strftime('%d/%m/%Y', dt.data_chegada) AS data_chegada,
            ROUND(dt.km_rodado, 2) AS km_rodado,
            ROUND((dt.km_rodado / dt.consumo_diesel), 1) AS desempenho
        FROM DadosTelemetria dt
        JOIN Veiculos v ON dt.id_veiculo = v.id_veiculo
        WHERE v.placa = ?
        ORDER BY dt.data_chegada DESC
    """, (placa,))

    resultados = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return resultados