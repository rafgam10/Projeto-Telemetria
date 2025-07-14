from database.database_config import conectar

def lista_empresas():
    # Lista Vazia de Objetos empresas;
    empresas_dados = []
    
    # Bloco para coletar dados do DB;
    with conectar() as conn:
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM Empresas;")
        datas = cursor.fetchall()
        
        for data in datas:
            empresa = {
                "id": data['id'],
                "nome": data['empresa'],
                "cnpj": data['cnpj']
            }
            empresas_dados.append(empresa)
    
    return empresas_dados