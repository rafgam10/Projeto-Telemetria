from database.database_config import conectar
from collections import defaultdict
from collections import defaultdict
from decimal import Decimal, getcontext

def calcular_notas_motoristas(conn, empresa_id):
    getcontext().prec = 8
    
    with conn.cursor(dictionary=True) as cursor:
        # 1. Obter data mais recente
        cursor.execute("SELECT MAX(data_final) FROM Motoristas WHERE empresa_id = %s", (empresa_id,))
        data_avaliacao = cursor.fetchone()["MAX(data_final)"]
        if not data_avaliacao:
            print("⚠️ Nenhum dado encontrado")
            return False

        # 2. Buscar todos os registros
        cursor.execute("""
            SELECT 
                m.id,
                m.nome,
                m.consumo_medio,
                v.marca,
                v.modelo,
                COALESCE(mc.meta_km_por_litro, 1.0) AS meta_veiculo
            FROM Motoristas m
            JOIN Veiculos v ON m.veiculo_id = v.id
            LEFT JOIN MetasConsumo mc ON 
                v.marca = mc.marca AND 
                v.modelo = mc.modelo AND 
                mc.empresa_id = m.empresa_id
            WHERE m.empresa_id = %s AND m.data_final = %s
        """, (empresa_id, data_avaliacao))
        
        registros = cursor.fetchall()
        if not registros:
            
            return False

        # 3. Processar motoristas
        motoristas = defaultdict(list)
        desempenhos = []
        
        for reg in registros:
            nome = reg['nome']
            consumo = Decimal(str(reg['consumo_medio'])) if reg['consumo_medio'] is not None else Decimal('0')
            meta = Decimal(str(reg['meta_veiculo']))
            
            motoristas[nome].append({
                'consumo': consumo,
                'meta': meta,
                'dados': reg
            })

        # 4. Calcular médias e desempenhos
        for nome, registros in motoristas.items():
            qtd = len(registros)
            
            if qtd > 1:
                # Caso especial (como Gildásio) - usa média de consumo e média de meta
                total_consumo = sum(r['consumo'] for r in registros)
                total_meta = sum(r['meta'] for r in registros)
                media_consumo = total_consumo / qtd
                media_meta = total_meta / qtd
                
                desempenhos.append({
                    'nome': nome,
                    'valor': media_consumo,
                    'meta': media_meta,
                    'tipo': 'multi'
                })
                
            else:

                consumo = registros[0]['consumo']
                meta = registros[0]['meta']
                
                desempenhos.append({
                    'nome': nome,
                    'valor': consumo,
                    'meta': meta,
                    'tipo': 'single'
                })

        # 5. Determinar base para nota 5 (melhor razão consumo/meta)
        try:
            # Encontra a melhor razão entre consumo e meta
            melhor_razao = max(
                (d['valor']/d['meta'] for d in desempenhos if d['valor'] > 0),
                default=1.0
            )
            

        except Exception as e:
            melhor_razao = Decimal('1.0')

        # 6. Calcular e atualizar notas
        atualizados = 0
        for d in desempenhos:
            try:
                if d['tipo'] == 'multi':
                    # Casos como Gildásio - nota baseada na própria média
                    nota = (d['valor'] / d['meta']) * 5
                else:
                    # Casos normais - nota proporcional ao melhor desempenho
                    razao = d['valor'] / d['meta']
                    nota = (razao / melhor_razao) * 5
                
                nota = min(5.0, max(0.0, float(round(nota, 2))))
                
                
                cursor.execute("""
                    UPDATE Motoristas
                    SET avaliacao = %s
                    WHERE nome = %s AND empresa_id = %s AND data_final = %s
                """, (nota, d['nome'], empresa_id, data_avaliacao))
                atualizados += 1
                
            except Exception as e:
                continue

        return True
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