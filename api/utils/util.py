from database.database_config import conectar
from collections import defaultdict

def atualizar_notas_motoristas_por_marca_modelo(conn, empresa_id, marca, modelo):
    with conn.cursor(dictionary=True) as cursor:
        # 1. Buscar a meta padrão (não usada diretamente, mas pode servir de fallback)
        cursor.execute(
            """
            SELECT meta_km_por_litro
            FROM MetasConsumo
            WHERE empresa_id = %s AND marca = %s AND modelo = %s
            """,
            (empresa_id, marca, modelo)
        )
        resultado = cursor.fetchone()
        meta_padrao = resultado["meta_km_por_litro"] if resultado else 0

        # 2. Obter data_final mais recente para este marca/modelo
        cursor.execute(
            """
            SELECT MAX(m.data_final) AS data_mais_recente
            FROM Motoristas m
            JOIN Veiculos v ON m.veiculo_id = v.id
            WHERE m.empresa_id = %s AND v.marca = %s AND v.modelo = %s
            """,
            (empresa_id, marca, modelo)
        )
        data_mais_recente = cursor.fetchone()["data_mais_recente"]
        if not data_mais_recente:
            print(f"⚠️ Nenhum dado recente encontrado para {marca} {modelo}")
            return

        # 3. Buscar todos os registros dessa data, marca e modelo
        cursor.execute(
            """
            SELECT 
                m.id AS registro_id,
                m.nome AS motorista_nome,
                v.id AS veiculo_id,
                v.consumo_medio,
                mc.meta_km_por_litro
            FROM Motoristas m
            JOIN Veiculos v ON m.veiculo_id = v.id
            LEFT JOIN MetasConsumo mc
              ON v.marca = mc.marca AND v.modelo = mc.modelo AND mc.empresa_id = m.empresa_id
            WHERE m.empresa_id = %s AND v.marca = %s AND v.modelo = %s AND m.data_final = %s
            """,
            (empresa_id, marca, modelo, data_mais_recente)
        )
        registros = cursor.fetchall()
        if not registros:
            print(f"⚠️ Nenhum registro encontrado para atualização ({marca} {modelo}) na data {data_mais_recente}.")
            return

        # 4. Agrupar por motorista pelo nome
        grupos = defaultdict(list)
        for r in registros:
            grupos[r["motorista_nome"]].append(r)

        # 5. Calcular médias e metas para cada motorista
        medias = {}        # motorista_nome -> media_consumo
        metas_base = {}    # motorista_nome -> meta_base (single ou média)
        candidatos_base5 = []

        for nome, regs in grupos.items():
            consumos = [r["consumo_medio"] for r in regs if r["consumo_medio"] is not None]
            metas = [r["meta_km_por_litro"] for r in regs if r["meta_km_por_litro"] is not None]

            # média de consumo sempre
            media_consumo = sum(consumos) / len(consumos) if consumos else 0

            # meta base: média se mais de um, senão única, ou fallback
            if len(metas) > 1:
                meta_base = sum(metas) / len(metas)
            elif len(metas) == 1:
                meta_base = metas[0]
            else:
                meta_base = meta_padrao or 1

            medias[nome] = media_consumo
            metas_base[nome] = meta_base

            # candidato a nota 5 se atingiu ou superou sua meta
            if media_consumo >= meta_base:
                candidatos_base5.append(media_consumo)

        # 6. Definir a régua para nota 5
        if candidatos_base5:
            base_para_nota_5 = max(candidatos_base5)
        else:
            # se ninguém atingiu, usa maior meta_base
            base_para_nota_5 = max(metas_base.values(), default=meta_padrao or 1)

        # 7. Atualizar avaliações
        for nome, regs in grupos.items():
            media_consumo = medias[nome]
            if media_consumo == 0:
                nota = 0.0
            else:
                nota = round((media_consumo / base_para_nota_5) * 5, 2)

            # aplicar mesma nota a todos os registros deste motorista
            cursor.execute(
                """
                UPDATE Motoristas
                SET avaliacao = %s
                WHERE nome = %s AND empresa_id = %s AND data_final = %s
                """,
                (nota, nome, empresa_id, data_mais_recente)
            )

        print(f"✅ Notas atualizadas para {len(grupos)} motoristas ({marca} {modelo}) na data {data_mais_recente}.")

def top_motoristas(empresa_id, limite=100):
    conn = conectar()
    with conn.cursor(dictionary=True) as cursor:
        # Obter a data_final mais recente
        cursor.execute("""
            SELECT MAX(data_final) AS data_mais_recente
            FROM Motoristas
            WHERE empresa_id = %s
        """, (empresa_id,))
        data_result = cursor.fetchone()
        data_mais_recente = data_result["data_mais_recente"]

        if not data_mais_recente:
            print("⚠️ Nenhum dado recente encontrado.")
            return []

        # Buscar top motoristas da semana mais recente
        cursor.execute("""
            SELECT m.nome, m.avaliacao, v.placa, v.marca, v.modelo
            FROM Motoristas m
            JOIN Veiculos v ON m.veiculo_id = v.id
            WHERE m.empresa_id = %s AND m.data_final = %s
            ORDER BY m.avaliacao DESC
            LIMIT %s
        """, (empresa_id, data_mais_recente, limite))
        
        return cursor.fetchall()
