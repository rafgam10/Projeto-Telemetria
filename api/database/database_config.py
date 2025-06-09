import mysql.connector
from datetime import datetime

# Função para conectar ao banco
def conectar():
    return mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="root",
        database="DBTelemetria"
    )

# Obter todos os dados da tabela DadosTelemetria
def obter_dados():
    with conectar() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM DadosTelemetria;")
        return cursor.fetchall()

# Obter todas as placas de veículos (Utilizado)
def obter_placas():
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT placa FROM Veiculos;")
        return [placa[0].upper() for placa in cursor.fetchall()]

# Obter empresas (Utilizado)
def obter_empresas():
    with conectar() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Empresas;")
        return cursor.fetchall()

# Obter todos os motoristas
def obter_motoristas():
    with conectar() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Motoristas;")
        return cursor.fetchall()

# Obter todos os veículos (Utilizado)
def obter_veiculos():
    with conectar() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Veiculos;")
        return cursor.fetchall()

# Obter dados de veículo por placa (Utilizado)
def obter_dados_por_placa(placa):
    with conectar() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT v.*, m.nome AS motorista_nome
            FROM Veiculos v
            LEFT JOIN Motoristas m ON m.veiculo_id = v.id
            WHERE UPPER(v.placa) = %s;
        """, (placa.upper(),))
        return cursor.fetchall()

# Obter metas de consumo
def obter_metas_consumo():
    with conectar() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM MetasConsumo;")
        return cursor.fetchall()

# Obter relatório de motoristas por empresa
def obter_relatorio_motoristas(id_empresa):
    with conectar() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                m.id AS id_motorista,
                m.nome,
                COUNT(v.id) AS total_veiculos,
                COALESCE(SUM(m.distancia_total), 0) AS distancia_total,
                m.marcha_lenta_total,
                COALESCE(SUM(m.consumo_total), 0) AS consumo_total,
                COALESCE(AVG(m.consumo_medio), 0) AS consumo_medio
            FROM Motoristas m
            JOIN Veiculos v ON m.veiculo_id = v.id
            WHERE v.empresa_id = %s
            GROUP BY m.id, m.nome, m.marcha_lenta_total
            ORDER BY m.nome;
        """, (id_empresa,))
        return cursor.fetchall()

# Inserir uma nova empresa (Utilizado)
def add_empresa(nome, cnpj):
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Empresas (nome, cnpj)
            VALUES (%s, %s)
        """, (nome, cnpj))
        conn.commit()
    return "Empresa adicionada com sucesso"


# Coletada dados distancia_semanal:
def distancia_semanal_func(empresa_id):
        with conectar() as conn:
            cursor = conn.cursor(dictionary=True)

            cursor.execute("""
                SELECT 
                    WEEK(data_inicial) AS semana,
                    YEAR(data_inicial) AS ano,
                    SUM(distancia_viagem) AS total_km
                FROM Veiculos
                WHERE empresa_id = %s AND data_inicial IS NOT NULL
                GROUP BY ano, semana
                ORDER BY ano, semana
            """, (empresa_id,))
            
            return cursor.fetchall()

# Coleta de dados media_semanal_frota:
def media_semanal_frota_func(empresa_id):
    with conectar() as conn:
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT 
                v.frota,
                WEEK(v.data_inicial) AS semana,
                YEAR(v.data_inicial) AS ano,
                ROUND(AVG(v.distancia_viagem), 2) AS media_km
            FROM Veiculos v
            WHERE v.empresa_id = %s
            GROUP BY v.frota, ano, semana
            ORDER BY v.frota, ano, semana
        """, (empresa_id,))
        
        return cursor.fetchall()
    
def soma_km_semanal_func(empresa_id):
    with conectar() as conn:
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT 
                MONTH(data_inicial) AS mes,
                YEAR(data_inicial) AS ano,
                WEEK(data_inicial) AS semana,
                SUM(distancia_viagem) AS total_km
            FROM Veiculos
            WHERE empresa_id = %s
            GROUP BY ano, mes, semana
            ORDER BY ano, mes, semana
        """, (empresa_id,))
        
        return cursor.fetchall()
    
# Coleta de Dados do Motorista (Utilizado)
def motorista_info_func(motorista_id):
    with conectar() as conn:
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT 
                m.id,
                m.nome,
                m.distancia_total,
                TIME_FORMAT(m.marcha_lenta_total, '%%H:%%i:%%s') AS marcha_lenta_total,
                m.consumo_total,
                m.consumo_medio,
                m.avaliacao,
                v.placa AS veiculo
            FROM Motoristas m
            LEFT JOIN Veiculos v ON m.veiculo_id = v.id
            WHERE m.id = %s
        """, (motorista_id,))

        return cursor.fetchone()
    
def veiculo_info_func(veiculo_id):
    with conectar() as conn:
        cursor = conn.cursor(dictionary=True)

        cursor.execute(f"""
            SELECT 
                v.id,
                v.placa,
                v.frota,
                v.marca,
                v.modelo,
                DATE_FORMAT(v.data_inicial, '%d/%m/%Y') AS data_inicial,
                DATE_FORMAT(v.data_final, '%d/%%m/%Y') AS data_final,
                v.distancia_viagem,
                v.velocidade_maxima,
                v.velocidade_media,
                v.litros_consumidos,
                v.consumo_medio,
                TIME_FORMAT(v.tempo_marcha_lenta, '%%H:%%i:%%s') AS tempo_marcha_lenta,
                e.nome AS empresa
            FROM Veiculos v
            LEFT JOIN Empresas e ON v.empresa_id = e.id
            WHERE v.id = {veiculo_id}
        """, ())
        
        return cursor.fetchone()    


def consumo_semanal_empresa_func(id_empresa):
    
    with conectar() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT
                data_inicial,
                data_final,
                ROUND(AVG(consumo_medio), 2) AS consumo_medio
            FROM Motoristas
            WHERE empresa_id = %s
            GROUP BY data_inicial, data_final
            ORDER BY data_final DESC
            LIMIT 4
        """, (id_empresa,))

        return cursor.fetchall()
    
