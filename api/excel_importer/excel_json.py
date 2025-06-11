# utils/importacao_excel.py
import pandas as pd
import os
from database.database_config import conectar
from datetime import datetime

def importar_dados_excel_mysql(caminho_arquivo, empresa_id):
    df = pd.read_excel(caminho_arquivo, engine="openpyxl", skiprows=2)
    df = df.dropna(how='all')  # Remove linhas totalmente vazias

    df.columns = [
        "motorista_uf", "marca", "modelo", "frota_placa",
        "ano_fabricacao", "km", "ltrs", "media_geral", "data_inicio", "data_final"
    ]

    registros_inseridos = 0

    conn = conectar()

    try:
        with conn.cursor(dictionary=True) as cursor:
            for _, row in df.iterrows():
                # Garantir valores válidos
                PlacaEFrota = str(row["frota_placa"]).split(' - ')
                frota = str(PlacaEFrota[0])
                placa = str(PlacaEFrota[1])
                marca = str(row["marca"]).strip()
                modelo = str(row["modelo"]).strip()
                data_inicio = pd.to_datetime(row["data_inicio"], errors='coerce').date() if not pd.isna(row["data_inicio"]) else None
                data_final = pd.to_datetime(row["data_final"], errors='coerce').date() if not pd.isna(row["data_final"]) else None
                km = float(row["km"]) if not pd.isna(row["km"]) else 0
                litros = float(row["ltrs"]) if not pd.isna(row["ltrs"]) else 0
                media = float(row["media_geral"]) if not pd.isna(row["media_geral"]) else 0
                nome_motorista = str(row["motorista_uf"]).strip()

                print(f"Processando: {nome_motorista} | Frota: {frota} | Placa: {placa}")

                # 1️⃣ Verificar se o veículo já existe
                sql_veiculo = "SELECT id FROM Veiculos WHERE placa = %s AND empresa_id = %s"
                cursor.execute(sql_veiculo, (placa, empresa_id))
                veiculo = cursor.fetchone()

                if veiculo:
                    veiculo_id = veiculo["id"]
                else:
                    sql_insert_veiculo = """
                        INSERT INTO Veiculos (placa, frota, marca, modelo, data_inicial, data_final, litros_consumidos, consumo_medio, empresa_id)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(sql_insert_veiculo, (
                        placa, frota, marca, modelo, data_inicio, data_final,
                        litros, media, empresa_id
                    ))
                    veiculo_id = cursor.lastrowid
                    print("Veiculos foi!")

                # 2️⃣ Inserir motorista vinculado ao veículo
                sql_insert_motorista = """
                    INSERT INTO Motoristas (
                        nome, data_inicial, data_final, veiculo_id, empresa_id,
                        distancia_total, marcha_lenta_total, consumo_total, consumo_medio
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql_insert_motorista, (
                    nome_motorista,
                    data_inicio,
                    data_final,
                    veiculo_id,
                    empresa_id,
                    km,
                    "00:00:00",  # marcha lenta placeholder
                    litros,
                    media
                ))

                registros_inseridos += 1

        conn.commit()
        print("Finalizando com Sucesso", 200)
    except Exception as e:
        print("Erro ao importar:", e)
        conn.rollback()
    finally:
        conn.close()
        if os.path.exists(caminho_arquivo):
            os.remove(caminho_arquivo)

    return registros_inseridos