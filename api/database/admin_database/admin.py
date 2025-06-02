from database.database_util import conectar
from datetime import datetime
import sqlite3

def obter_motoristas_completo(id_empresa):
    conn = conectar()
    cursor = conn.cursor()

    # Monta filtro por empresa
    filtro_empresa = ""
    params = []
    if id_empresa:
        filtro_empresa = "WHERE m.id_empresa = ?"
        params.append(id_empresa)

    # Query para obter dados principais dos motoristas e último veículo da empresa (exemplo)
    # Nota: aqui supomos que veículo é da empresa; pra ligar veículo ao motorista precisaria relacionamento explícito
    cursor.execute(f"""
        SELECT 
            m.id_motorista,
            m.nome,
            m.avaliacao,
            m.status,
            -- Veículo mais recente da empresa (pode adaptar)
            v.marca || ' / ' || v.modelo || ' / ' || v.placa as caminhao,
            -- Última viagem (data_chegada) e km_rodado da última viagem
            (SELECT data_chegada FROM DadosTelemetria dt WHERE dt.id_motorista = m.id_motorista ORDER BY data_chegada DESC LIMIT 1) AS ultima_data,
            (SELECT km_rodado FROM DadosTelemetria dt WHERE dt.id_motorista = m.id_motorista ORDER BY data_chegada DESC LIMIT 1) AS km_ultima_viagem,
            -- Consumo médio diesel e arla em km por litro (calculado com médias das viagens)
            (SELECT AVG(consumo_diesel * 100.0 / km_rodado) FROM DadosTelemetria dt WHERE dt.id_motorista = m.id_motorista AND km_rodado > 0) AS consumo_diesel_100km,
            (SELECT AVG(consumo_arla * 100.0 / km_rodado) FROM DadosTelemetria dt WHERE dt.id_motorista = m.id_motorista AND km_rodado > 0) AS consumo_arla_100km
        FROM Motoristas m
        LEFT JOIN Veiculos v ON v.id_empresa = m.id_empresa
        {filtro_empresa}
        GROUP BY m.id_motorista
        ORDER BY m.nome
    """, params)

    resultados = cursor.fetchall()
    conn.close()

    lista_motoristas = []
    for (id_mot, nome, avaliacao, status, caminhao, ultima_data, km_ultima, cons_diesel, cons_arla) in resultados:
        # Formata data
        if ultima_data:
            try:
                dt = datetime.strptime(ultima_data, "%Y-%m-%d %H:%M:%S")
                ultima_data_fmt = dt.strftime("%d/%m/%Y %H:%M")
            except Exception:
                ultima_data_fmt = ultima_data
        else:
            ultima_data_fmt = "N/A"

        # Formata consumo
        if cons_diesel and cons_arla:
            consumo_fmt = f"{cons_diesel:.1f}K/100Km e {cons_arla:.1f}L/100Km"
        else:
            consumo_fmt = "N/A"

        lista_motoristas.append({
            "id": id_mot,
            "nome": nome,
            "caminhao": caminhao or "N/A",
            "ultima_viagem": f"{ultima_data_fmt} {km_ultima:.1f}Km" if km_ultima else "N/A",
            "avaliacao": round(avaliacao, 1) if avaliacao else "N/A",
            "consumo": consumo_fmt,
            "status": status or "N/A"
        })

    return lista_motoristas

# Gestão Motoristas:
def motorista_dados_unicos(id_empresa):
    conn = conectar()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            m.id_motorista,
            m.nome AS nome_motorista,
            v.marca || ' / ' || v.modelo AS caminhao,
            v.placa,
            strftime('%d/%m/%Y', MAX(dt.data_saida)) AS ultima_viagem_data,
            ROUND(dt.km_rodado, 2) AS km_ultima_viagem,
            ROUND(AVG(m.avaliacao), 1) AS avaliacao_media,
            ROUND(AVG(dt.consumo_diesel), 1) AS consumo_diesel_medio,
            ROUND(AVG(dt.consumo_arla), 1) AS consumo_arla_medio,
            m.status,
            strftime('%d/%m/%Y', dt.data_registro) AS data_Registro
        FROM DadosTelemetria dt
        JOIN Motoristas m ON dt.id_motorista = m.id_motorista
        JOIN Veiculos v ON dt.id_veiculo = v.id_veiculo
        WHERE dt.id_empresa = ?
        GROUP BY m.id_motorista
        ORDER BY m.nome
    """, (id_empresa,))
    
    resultados = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return resultados

# Dados do Motorista e Veiculos apenas 1: 
def motorista_dados_unicos_editar(id_motorista):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            m.id_motorista,
            m.nome,
            m.status,
            v.id_veiculo,
            v.placa,
            v.marca,
            v.modelo
        FROM Motoristas m
        JOIN DadosTelemetria dt ON m.id_motorista = dt.id_motorista
        JOIN Veiculos v ON dt.id_veiculo = v.id_veiculo
        WHERE m.id_motorista = ?
        LIMIT 1
    """, (id_motorista,))

    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            "id_motorista": row[0],
            "nome": row[1],
            "status": row[2],
            "id_veiculo": row[3],
            "placa": row[4],
            "marca": row[5],
            "modelo": row[6]
        }
    else:
        return None

# Gestão de Veiculos

def veiculo_dados_unicos(id_empresa):
    conn = conectar()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            v.id_veiculo,
            v.marca || ' / ' || v.modelo AS caminhao,
            v.placa,
            v.frota,
            ROUND(AVG(dt.km_rodado / NULLIF(dt.consumo_diesel, 0)), 1) || ' Km/L' AS media_km_por_litro,
            ROUND(MAX(dt.km_rodado), 1) AS km_atual,
            strftime('%d/%m/%Y', MAX(dt.data_saida)) AS ultima_manutencao,
            v.status
        FROM Veiculos v
        JOIN DadosTelemetria dt ON v.id_veiculo = dt.id_veiculo
        WHERE dt.id_empresa = ?
        GROUP BY v.id_veiculo
        ORDER BY v.marca, v.modelo
    """, (id_empresa,))
    
    resultados = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return resultados


# INSERT de Dados do Motorista:
def adicionar_motorista_banco(nome, cpf, cnh, data_nascimento, id_empresa):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Motoristas (nome, cpf, cnh, data_nascimento, id_empresa)
        VALUES (?, ?, ?, ?, ?)
    """, (nome, cpf, cnh, data_nascimento, id_empresa))
    conn.close()
    return