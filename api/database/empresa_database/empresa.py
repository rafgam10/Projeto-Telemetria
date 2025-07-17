from database.database_config import conectar
import mysql.connector

def lista_empresas_db():
    empresas_dados = []  # Garante que a variável está dentro da função
    try:
        with conectar() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT id, nome, cnpj FROM Empresas ORDER BY nome;")
                for data in cursor.fetchall():
                    empresas_dados.append({
                        "id": data["id"],
                        "nome": data["nome"],
                        "cnpj": data["cnpj"]
                    })
    except Exception as e:
        print(f"Erro ao buscar empresas: {e}")
    
    return empresas_dados

# def deletar_empresa(id):
#     try:
#         with conectar() as conn:
#             with conn.cursor() as cursor:
#                 cursor = conn.cursor(dictionary=True)
#                 cursor.execute("DELETE FROM Empresas WHERE id = ?", (id,))
#                 return
        
#     except mysql.connector.Error as e:
#         print(f"[ERRO BANCO] Falha ao deletar empresa: {e}")
#         return e