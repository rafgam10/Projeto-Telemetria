from database.database_config import conectar

def atualizar_notas_motoristas_por_marca_modelo(conn, empresa_id, marca, modelo):
    with conn.cursor(dictionary=True) as cursor:
        cursor.execute("""
            SELECT meta_km_por_litro
            FROM MetasConsumo
            WHERE empresa_id = %s AND marca = %s AND modelo = %s
        """, (empresa_id, marca, modelo))
        resultado = cursor.fetchone()

        if not resultado:
            print(f"⚠️ Meta não encontrada para {marca} {modelo}")
            return

        meta = resultado["meta_km_por_litro"]

        cursor.execute("""
            SELECT id, consumo_medio
            FROM Veiculos
            WHERE empresa_id = %s AND marca = %s AND modelo = %s
        """, (empresa_id, marca, modelo))
        veiculos = cursor.fetchall()

        for veiculo in veiculos:
            veiculo_id = veiculo["id"]
            consumo_real = veiculo["consumo_medio"]
            nota = 1.0 if not consumo_real or not meta else round(max(0.0, min(5.0, (consumo_real / meta) * 5)), 2)

            cursor.execute("""
                UPDATE Motoristas
                SET avaliacao = %s
                WHERE veiculo_id = %s AND empresa_id = %s
            """, (nota, veiculo_id, empresa_id))
        
        print(f"✅ Notas atualizadas para veículos {marca} {modelo}.")


def top_motoristas(empresa_id, limite=5):
    conn = conectar()
    with conn.cursor(dictionary=True) as cursor:
        cursor.execute("""
            SELECT m.nome, m.avaliacao, v.placa, v.marca, v.modelo
            FROM Motoristas m
            JOIN Veiculos v ON m.veiculo_id = v.id
            WHERE m.empresa_id = %s
            ORDER BY m.avaliacao DESC
            LIMIT %s
        """, (empresa_id, limite))
        
        return cursor.fetchall()
