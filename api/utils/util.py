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
