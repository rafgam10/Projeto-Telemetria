from database.database_config import conectar
from collections import defaultdict
from decimal import Decimal, getcontext

from collections import defaultdict
from decimal import Decimal, getcontext
from typing import Any, Dict

def calcular_notas_motoristas(conn, empresa_id) -> Dict[str, Any]:
    """
    Calcula e atualiza avaliacao apenas para os registros correspondentes à
    ÚLTIMA importação de CADA motorista (baseado em nome + data_final máxima por nome).
    Regras de nota:
      - Se pelo menos um motorista tiver valor >= meta, normaliza pelo melhor ratio.
      - Se nenhum motorista bater a meta, cada nota = (valor/meta) * 5 (nenhum recebe 5 automaticamente).
    Retorna dicionário com resultado e contagem de atualizações.
    """
    getcontext().prec = 8
    warnings = []

    with conn.cursor(dictionary=True) as cursor:
        # 1) pegar lista (nome, max(data_final)) por motorista para a empresa
        cursor.execute("""
            SELECT nome, MAX(data_final) AS ultima_data
            FROM Motoristas
            WHERE empresa_id = %s
            GROUP BY nome
        """, (empresa_id,))
        latest_per_name = cursor.fetchall()
        if not latest_per_name:
            return {"success": False, "reason": "Nenhum registro de motorista encontrado para a empresa", "updated": 0}

        # 2) construir subconsulta JOIN para obter apenas os registros que são a última importação de cada nome
        #    (se houver múltiplos registros com mesma nome+data_final, todos serão retornados — depois agrupamos)
        # Usamos JOIN com a subquery para compatibilidade ampla.
        cursor.execute("""
            SELECT
                m.nome,
                m.consumo_medio,
                v.marca,
                v.modelo,
                COALESCE(mc.meta_km_por_litro, NULL) AS meta_veiculo,
                m.data_final
            FROM Motoristas m
            JOIN (
                SELECT nome, MAX(data_final) AS ultima_data
                FROM Motoristas
                WHERE empresa_id = %s
                GROUP BY nome
            ) ult ON m.nome = ult.nome AND m.data_final = ult.ultima_data
            LEFT JOIN Veiculos v ON m.veiculo_id = v.id
            LEFT JOIN MetasConsumo mc
                ON v.marca = mc.marca
                AND v.modelo = mc.modelo
                AND mc.empresa_id = m.empresa_id
            WHERE m.empresa_id = %s
        """, (empresa_id, empresa_id))

        registros = cursor.fetchall()
        if not registros:
            return {"success": False, "reason": "Nenhum registro encontrado nas últimas importações por nome", "updated": 0}

        # 3) agrupar por nome -> lista de registros (pode haver mais de 1 se houver múltiplos veículos/linhas na mesma última data)
        agrupado = defaultdict(list)
        for r in registros:
            nome = r['nome']
            consumo = Decimal(str(r['consumo_medio'])) if r['consumo_medio'] is not None else Decimal('0')
            meta_raw = r.get('meta_veiculo')
            meta = Decimal(str(meta_raw)) if meta_raw is not None else None
            agrupado[nome].append({
                'consumo': consumo,
                'meta': meta,
                'data_final': r['data_final']
            })

        # 4) construir lista de desempenhos por nome (média quando múltiplos registros na mesma última data)
        desempenhos = []
        for nome, items in agrupado.items():
            qtd = len(items)
            total_consumo = sum(i['consumo'] for i in items)
            metas_validas = [i['meta'] for i in items if i['meta'] is not None and i['meta'] > 0]

            valor = total_consumo / qtd

            if metas_validas:
                media_meta = sum(metas_validas) / Decimal(len(metas_validas))
            else:
                # fallback seguro: evita divisão por zero; avisamos para que você possa corrigir os dados
                warnings.append(f"motorista '{nome}' não tem meta válida; usando meta=1 como fallback")
                media_meta = Decimal('1')

            # guardamos a data_final (todas as entradas em items têm a mesma data_final, pois foi selecionado assim)
            data_final = items[0]['data_final']

            desempenhos.append({
                'nome': nome,
                'valor': valor,
                'meta': media_meta,
                'data_final': data_final
            })

        # 5) decidir estratégia: alguém bateu a meta?
        alguem_bateu_meta = any(d['valor'] >= d['meta'] for d in desempenhos if d['meta'] and d['meta'] > 0)

        # 6) calcular melhor_razao se necessário
        if alguem_bateu_meta:
            ratios = [ (d['valor'] / d['meta']) for d in desempenhos if d['meta'] and d['valor'] > 0 ]
            melhor_razao = max(ratios) if ratios else Decimal('1')
        else:
            melhor_razao = None

        # 7) calcular notas e atualizar apenas os registros correspondentes àquele nome+data_final
        atualizados = 0
        for d in desempenhos:
            try:
                ratio = (d['valor'] / d['meta']) if d['meta'] and d['meta'] > 0 else Decimal('0')

                if ratio <= 0:
                    nota = Decimal('0')
                else:
                    if alguem_bateu_meta:
                        nota = (ratio / melhor_razao) * Decimal('5')
                    else:
                        nota = ratio * Decimal('5')

                # arredondar para 2 casas e limitar entre 0 e 5
                nota = max(Decimal('0'), min(Decimal('5'), nota.quantize(Decimal('0.01'))))
                nota_float = float(nota)

                # UPDATE usando nome + empresa_id + data_final (conforme sua regra)
                cursor.execute("""
                    UPDATE Motoristas
                    SET avaliacao = %s
                    WHERE nome = %s AND empresa_id = %s AND data_final = %s
                """, (nota_float, d['nome'], empresa_id, d['data_final']))

                # rowcount pode não existir em alguns adaptadores; usamos fallback
                atualizados += cursor.rowcount if hasattr(cursor, 'rowcount') and cursor.rowcount is not None else 1
            except Exception as e:
                warnings.append(f"erro ao atualizar '{d['nome']}' (data {d['data_final']}): {e}")
                continue

        # 8) commit se possível
        try:
            if hasattr(conn, "commit"):
                conn.commit()
        except Exception as e:
            warnings.append(f"commit falhou: {e}")

        return {
            "success": True,
            "updated": atualizados,
            "n_motoristas": len(desempenhos),
            "alguem_bateu_meta": bool(alguem_bateu_meta),
            "warnings": warnings
        }





def top_motoristas(empresa_id, limite=None):
    """Retorna os motoristas da última data, com média para múltiplos registros e nomes limpos"""
    conn = conectar()
    with conn.cursor(dictionary=True) as cursor:
        # 1. Obter a data_final mais recente
        cursor.execute("""
            SELECT MAX(data_final) AS data_mais_recente
            FROM Motoristas
            WHERE empresa_id = %s
        """, (empresa_id,))
        data_result = cursor.fetchone()
        data_mais_recente = data_result["data_mais_recente"]

        if not data_mais_recente:
            return []

        # 2. Buscar todos os registros
        cursor.execute("""
            SELECT 
                m.id,
                m.nome,
                m.avaliacao,
                v.placa,
                v.marca, 
                v.modelo,
                COUNT(*) OVER (PARTITION BY m.nome) AS qtd_registros
            FROM Motoristas m
            JOIN Veiculos v ON m.veiculo_id = v.id
            WHERE m.empresa_id = %s AND m.data_final = %s
            ORDER BY m.avaliacao DESC
        """, (empresa_id, data_mais_recente))
        
        registros = cursor.fetchall()
        
        # 3. Processar resultados para agrupar os com múltiplos registros
        resultados = []
        motoristas_processados = set()
        
        for reg in registros:
            # Processar nome para remover código e estado
            nome_original = reg['nome']
            nome_limpo = nome_original.split('[')[0].split(']')[-1].strip()  # Remove estado
            nome_limpo = nome_limpo.split('-')[-1].strip()  # Remove código
            
            if nome_limpo in motoristas_processados:
                continue
                
            if reg['qtd_registros'] > 1:
                # Calcular média para motoristas com múltiplos registros
                cursor.execute("""
                    SELECT AVG(avaliacao) AS media_avaliacao
                    FROM Motoristas
                    WHERE nome = %s AND data_final = %s AND empresa_id = %s
                """, (nome_original, data_mais_recente, empresa_id))
                media = cursor.fetchone()['media_avaliacao']
                
                resultados.append({
                    'nome': nome_limpo,  # Usa o nome limpo
                    'avaliacao': float(round(media, 2)),
                    'placa': 'Vários veículos',
                    'marca': reg['marca'],
                    'modelo': reg['modelo']
                })
            else:
                # Manter avaliação individual
                resultados.append({
                    'nome': nome_limpo,  # Usa o nome limpo
                    'avaliacao': reg['avaliacao'],
                    'placa': reg['placa'],
                    'marca': reg['marca'],
                    'modelo': reg['modelo']
                })
                
            motoristas_processados.add(nome_limpo)
        
        # 4. Aplicar limite se especificado
        if limite:
            return resultados[:limite]
        return resultados