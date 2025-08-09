import pandas as pd
import traceback
from database.database_config import conectar
from utils.util import calcular_notas_motoristas

def calcular_nota_por_meta(consumo_real, meta):
    if not consumo_real or not meta or meta == 0:
        return 1.0
    nota = (consumo_real / meta) * 5
    return round(max(0.0, min(5.0, nota)), 2)


def importar_dados_excel_mysql(caminho_arquivo, empresa_id):
    df = pd.read_excel(caminho_arquivo.strip(), engine="openpyxl", skiprows=2)
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
            print("🚀 Iniciando importação...")

            # Usa a primeira linha como data da importação
            data_inicio_import = pd.to_datetime(df.iloc[0]["data_inicio"], errors='coerce').date()
            data_final_import = pd.to_datetime(df.iloc[0]["data_final"], errors='coerce').date()

            # Insere registro da importação e pega o ID
            cursor.execute("""
                INSERT INTO Importacoes (data_inicial, data_final, qtd_itens, empresa_id)
                VALUES (%s, %s, %s, %s)
            """, (data_inicio_import, data_final_import, 0, empresa_id))
            importacao_id = cursor.lastrowid

            for _, row in df.iterrows():
                PlacaEFrota = str(row["frota_placa"]).replace("–", "-").split(" - ")
                if len(PlacaEFrota) < 2:
                    print(f"⚠️ Formato inválido para frota_placa: {row['frota_placa']}")
                    continue

                frota = PlacaEFrota[0].strip()
                placa = PlacaEFrota[1].strip()
                marca = str(row["marca"]).strip()
                modelo = str(row["modelo"]).strip()
                data_inicio = pd.to_datetime(row["data_inicio"], errors='coerce').date()
                data_final = pd.to_datetime(row["data_final"], errors='coerce').date()
                km = float(str(row["km"]).replace(',', '.')) if not pd.isna(row["km"]) else 0
                litros = float(str(row["ltrs"]).replace(',', '.')) if not pd.isna(row["ltrs"]) else 0
                media = float(str(row["media_geral"]).replace(',', '.')) if not pd.isna(row["media_geral"]) else 0
                nome_motorista = str(row["motorista_uf"]).strip()

                # Verifica ou insere veículo
                cursor.execute("SELECT id FROM Veiculos WHERE placa = %s AND empresa_id = %s", (placa, empresa_id))
                veiculo = cursor.fetchone()
                if veiculo:
                    veiculo_id = veiculo["id"]
                else:
                    cursor.execute("""
                        INSERT INTO Veiculos (placa, frota, marca, modelo, data_inicial, data_final, litros_consumidos, consumo_medio, empresa_id, importacao_id)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        placa, frota, marca, modelo, data_inicio, data_final,
                        litros, media, empresa_id, importacao_id
                    ))
                    veiculo_id = cursor.lastrowid

                veiculos_afetados.add(veiculo_id)

                # Insere motorista
                nota = calcular_nota_por_meta(media, media)
                cursor.execute("""
                    INSERT INTO Motoristas (
                        nome, data_inicial, data_final, veiculo_id, empresa_id,
                        distancia_total, marcha_lenta_total, consumo_total,
                        consumo_medio, avaliacao, importacao_id
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    nome_motorista,
                    data_inicio,
                    data_final,
                    veiculo_id,
                    empresa_id,
                    km,
                    "00:00:00",
                    litros,
                    media,
                    nota,
                    importacao_id
                ))

                registros_inseridos += 1

                # Garante que meta existe
                cursor.execute("""
                    SELECT id FROM MetasConsumo WHERE empresa_id = %s AND marca = %s AND modelo = %s
                """, (empresa_id, marca, modelo))
                meta_existente = cursor.fetchone() # Registro UNICO;
                if not meta_existente:
                    cursor.execute("""
                        INSERT INTO MetasConsumo (empresa_id, marca, modelo, meta_km_por_litro)
                        VALUES (%s, %s, %s, %s)
                    """, (empresa_id, marca, modelo, 1))

                calcular_notas_motoristas(conn, empresa_id)
            # # Recalcula notas
            # for veiculo_id in veiculos_afetados:
            #     cursor.execute("""
            #         SELECT v.id, v.consumo_medio AS consumo_real, v.marca, v.modelo
            #         FROM Veiculos v
            #         WHERE v.id = %s AND v.empresa_id = %s
            #     """, (veiculo_id, empresa_id))
            #     v = cursor.fetchone()
            #     cursor.execute("""
            #         SELECT meta_km_por_litro FROM MetasConsumo
            #         WHERE empresa_id = %s AND marca = %s AND modelo = %s
            #     """, (empresa_id, v["marca"], v["modelo"]))
            #     meta = cursor.fetchone()
            #     if meta:
            #         nota = calcular_nota_por_meta(v["consumo_real"], meta["meta_km_por_litro"])
            #         cursor.execute("""
            #             UPDATE Motoristas
            #             SET avaliacao = %s
            #             WHERE veiculo_id = %s AND empresa_id = %s
            #         """, (nota, veiculo_id, empresa_id))

            # Atualiza a quantidade de itens importados
            cursor.execute("UPDATE Importacoes SET qtd_itens = %s WHERE id = %s", (registros_inseridos, importacao_id))

        conn.commit()
        print(f"✅ Finalizado. {registros_inseridos} registros inseridos.")
    except Exception as e:
        print("Erro ao importar:", e)
        traceback.print_exc()
        conn.rollback()
    finally:
        conn.close()

    return registros_inseridos
