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
            v.marca,
            v.modelo,
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


####################################################################

# Adicionar um Novo Motorista e Veiculos:
def adicionar_motorista_banco(nome, cpf, cnh, nascimento, status, id_empresa):
    conn = conectar()  # Sua função conectar() deve abrir a conexão com timeout configurado
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Motoristas (nome, cpf, cnh, data_nascimento, status, id_empresa)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (nome, cpf, cnh, nascimento, status, id_empresa))
        conn.commit()
        id_motorista = cursor.lastrowid
        return id_motorista
    except sqlite3.OperationalError as e:
        print(f"Erro operacional no adicionar_motorista_banco: {e}")
        return None
    finally:
        conn.close()


def adicionar_veiculo_banco(placa, modelo, marca, ano, frota, km_atual,
                            media_km_litro, ultima_manutencao, status_veiculo
                            , empresa_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Veiculos (
            placa, modelo, marca, ano, frota,
            km_atual, media_km_litro, ultima_manutencao,
            status, id_empresa
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (placa, modelo, marca, ano, frota, km_atual, media_km_litro, ultima_manutencao, status_veiculo, empresa_id))

    conn.commit()
    id_veiculo = cursor.lastrowid  # <- IMPORTANTE
    conn.close()
    return id_veiculo  # <- CERTIFIQUE-SE DISSO
        
        
def adicionar_dados_telemetria_banco(id_empresa, id_motorista, id_veiculo,
                               data_saida, data_chegada,
                               hodometro_inicial, hodometro_final,
                               km_rodado, marcha_lenta,
                               lt_diesel_total, lt_arla_total, lt_por_dia):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO DadosTelemetria (
            id_empresa, id_motorista, id_veiculo,
            data_saida, data_chegada,
            hodometro_inicial, hodometro_final,
            km_rodado, marcha_lenta,
            lt_diesel_total, lt_arla_total, lt_por_dia
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        id_empresa, id_motorista, id_veiculo,
        data_saida, data_chegada,
        hodometro_inicial, hodometro_final,
        km_rodado, marcha_lenta,
        lt_diesel_total, lt_arla_total, lt_por_dia
    ))
    conn.commit()
    conn.close()
    
###########################################################################

############ Relatório #################

def dados_relatorios():
    con = conectar()
    cursor = con.cursor()

    # Buscar os últimos dados de telemetria por motorista e veículo
    cursor.execute("""
        SELECT 
            m.id_motorista,
            m.nome,
            v.placa,
            MAX(d.data_chegada) as ultima_data
        FROM DadosTelemetria d
        JOIN Motoristas m ON d.id_motorista = m.id_motorista
        JOIN Veiculos v ON d.id_veiculo = v.id_veiculo
        GROUP BY m.id_motorista, v.placa
    """)
    motoristas = cursor.fetchall()
    con.close()

    # Montar lista no formato desejado
    lista_motoristas = []
    for m in motoristas:
        try:
            id_motorista = str(m[0])
            nome_motorista = m[1]
            placa = m[2]
            lista_motoristas.append({
                "id": id_motorista,
                "nome": nome_motorista,
                "placa": placa
            })
        except Exception as e:
            print("Erro ao processar motorista:", e)
        
    return lista_motoristas



########## API motorista ID: ###################
def dados_por_id_motorista(id_motorista):
    con = conectar()
    cursor = con.cursor()

    # Buscar nome do motorista
    cursor.execute("""
        SELECT nome FROM Motoristas
        WHERE id_motorista = ?
    """, (id_motorista,))
    motorista = cursor.fetchone()

    if not motorista:
        con.close()
        return None  # Motorista não encontrado

    nome_motorista = motorista[0]

    # Buscar dados de telemetria
    cursor.execute("""
        SELECT data_chegada, media_km_l, total_hrs
        FROM DadosTelemetria
        WHERE id_motorista = ?
        ORDER BY data_chegada ASC
    """, (id_motorista,))
    
    registros = cursor.fetchall()
    con.close()

    if not registros:
        return None  # Nenhum dado encontrado

    lista_dados = []
    for data_chegada, media_km_l, total_hrs in registros:
        lista_dados.append({
            "data_chegada": data_chegada,
            "media_km_l": media_km_l,
            "total_hrs": total_hrs,
            "motorista": nome_motorista
        })

    return lista_dados