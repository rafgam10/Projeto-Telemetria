# utils/importacao_excel.py
import pandas as pd
import os
from database.database_config import conectar
from datetime import datetime


# Função para medir a nota do motorista baseada na meta
def calcular_nota_por_meta(consumo_real, meta):
    if not consumo_real or not meta or meta == 0:
        return 1.0
    nota = (consumo_real / meta) * 5
    return round(max(0.0, min(5.0, nota)), 2)


# Função principal de importação
def importar_dados_excel_mysql(caminho_arquivo, empresa_id):
    df = pd.read_excel(caminho_arquivo, engine="openpyxl", skiprows=2)
    df = df.dropna(how='all')

    df.columns = [
        "motorista_uf", "marca", "modelo", "frota_placa",
        "ano_fabricacao", "km", "ltrs", "media_geral", "data_inicio", "data_final"
    ]

    registros_inseridos = 0
    veiculos_afetados = set()

    conn = conectar()

    try:
        with conn.cursor(dictionary=True) as cursor:
            for _, row in df.iterrows():
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

                # 1️⃣ Verifica/insere veículo
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
                    print("Veículo inserido.")
                
                veiculos_afetados.add(veiculo_id)

                # 2️⃣ Insere motorista
                nota = calcular_nota_por_meta(media, media)  # Temporária, será recalculada abaixo

                sql_insert_motorista = """
                    INSERT INTO Motoristas (
                        nome, data_inicial, data_final, veiculo_id, empresa_id,
                        distancia_total, marcha_lenta_total, consumo_total, consumo_medio, avaliacao
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql_insert_motorista, (
                    nome_motorista,
                    data_inicio,
                    data_final,
                    veiculo_id,
                    empresa_id,
                    km,
                    "00:00:00",
                    litros,
                    media,
                    nota
                ))

                registros_inseridos += 1

                # 3️⃣ Garante meta existente
                cursor.execute("""
                    SELECT id FROM MetasConsumo WHERE empresa_id = %s AND marca = %s AND modelo = %s
                """, (empresa_id, marca, modelo))
                meta_existente = cursor.fetchone()

                if not meta_existente:
                    cursor.execute("""
                        INSERT INTO MetasConsumo (empresa_id, marca, modelo, meta_km_por_litro)
                        VALUES (%s, %s, %s, %s)
                    """, (empresa_id, marca, modelo, 1))
                    print(f"Meta registrada para {marca} {modelo} (padrão: 1 km/L)")

            # 4️⃣ Recalcular notas com base nas metas reais
            for veiculo_id in veiculos_afetados:
                cursor.execute("""
                    SELECT v.id, v.consumo_medio AS consumo_real, v.marca, v.modelo
                    FROM Veiculos v
                    WHERE v.id = %s AND v.empresa_id = %s
                """, (veiculo_id, empresa_id))
                v = cursor.fetchone()

                cursor.execute("""
                    SELECT meta_km_por_litro FROM MetasConsumo
                    WHERE empresa_id = %s AND marca = %s AND modelo = %s
                """, (empresa_id, v["marca"], v["modelo"]))
                meta = cursor.fetchone()

                if meta:
                    nota = calcular_nota_por_meta(v["consumo_real"], meta["meta_km_por_litro"])

                    cursor.execute("""
                        UPDATE Motoristas
                        SET avaliacao = %s
                        WHERE veiculo_id = %s AND empresa_id = %s
                    """, (nota, veiculo_id, empresa_id))

        conn.commit()
        print(f"Importação concluída com {registros_inseridos} registros inseridos e avaliações atualizadas.")

    except Exception as e:
        print("Erro ao importar:", e)
        conn.rollback()

    finally:
        conn.close()
        # if os.path.exists(caminho_arquivo):
        #     os.remove(caminho_arquivo)

    return registros_inseridos
