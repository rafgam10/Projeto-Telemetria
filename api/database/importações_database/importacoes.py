from ..database_config import conectar

def listar_importacoes_db(id_empresa):
    resultados = []
    with conectar() as conn:
        with conn.cursor(dictionary=True) as cursor:
            
            cursor.execute("SELECT * FROM Importacoes WHERE empresa_id = %s ORDER BY data_inicial DESC", (id_empresa,))
            datas = cursor.fetchall()
            
            for data in datas:
                resultados.append({
                    "id": data['id'],
                    'data_inicial': data['data_inicial'].strftime('%d/%m/%Y') if data['data_inicial'] else None,
                    'data_final': data['data_final'].strftime("%d/%m/%Y") if data['data_final'] else None,
                    'qtd_itens': data['qtd_itens'],
                    'empresa_id': data['empresa_id']
                })
    return resultados

def deletar_importacao_e_dados_relacionado_db(id_importacao) -> None:
    with conectar() as conn:
        with conn.cursor(dictionary=True) as cursor:
            
            cursor.execute("DELETE FROM Importacoes WHERE id = %s", (id_importacao,))
            conn.commit()
    
