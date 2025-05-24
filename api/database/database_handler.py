import sqlite3
import json

NOMETABELA = "DadosTelemetria"

def conectar():
    #return sqlite3.connect(f"Projeto-Telemetria/api/database/{NOMETABELA}.db")
    return sqlite3.connect(f"api/database/{NOMETABELA}.db")


def criar_tabela():
    conec = conectar()
    cursor = conec.cursor()
    cursor.execute(f"DROP TABLE IF EXISTS {NOMETABELA}")
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {NOMETABELA} (
            motorista TEXT,
            nr_acerto INTEGER,
            data TEXT,
            data_saida TEXT,
            data_chegada TEXT,
            km_saida REAL,
            km_chegada REAL,
            km_rodado REAL,
            km_vazio REAL,
            porcento_vazio REAL,
            qtd_dias INTEGER,
            total_hrs INTEGER,
            frota TEXT,
            placa TEXT,
            marca_modelo TEXT,
            ano_veiculo INTEGER,
            lt_diesel REAL,
            media REAL,
            lt_arla REAL,
            porcento_arla REAL,
            nr_equipamento INTEGER,
            marca_modelo_equipamento TEXT,
            ano_equipamento INTEGER,
            lt_diesel_equip REAL,
            media_1 REAL,
            media_2 REAL,
            lt_por_dia REAL,
            km_rodado_dup REAL,
            dif REAL,
            media_dup REAL,
            dif_media REAL
        )
    """)

    # cursor.execute(sql)

    conec.commit()
    cursor.close()

def inserir_dados(dados):
    conec = conectar(); cursor = conec.cursor()
    
    # Insere os dados
    for item in dados:
        cursor.execute(f"""
            INSERT INTO {NOMETABELA} (
                motorista, nr_acerto, data, data_saida, data_chegada,
                km_saida, km_chegada, km_rodado, km_vazio, porcento_vazio,
                qtd_dias, total_hrs, frota, placa, marca_modelo, ano_veiculo,
                lt_diesel, media, lt_arla, porcento_arla,
                nr_equipamento, marca_modelo_equipamento, ano_equipamento,
                lt_diesel_equip, media_1, media_2,
                lt_por_dia, km_rodado_dup, dif, media_dup, dif_media
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            item.get("MOTORISTA"),
            item.get("NR Acerto"),
            item.get("Data"),
            item.get("Data de Saida"),
            item.get("Data de Cheg."),
            item.get("Km Saída"),
            item.get("Km Cheg."),
            item.get("Km Rod."),
            item.get("Km Vazio"),
            item.get("% Vazio"),
            item.get("Qtd Dias"),
            item.get("Tot. Hrs"),
            item.get("Frota"),
            item.get("Placa"),
            item.get("Marca / Modelo"),
            item.get("Ano"),
            item.get("Lt. Diesel"),
            item.get("Méd."),
            item.get("Lt. Arla"),
            item.get("% ARLA"),
            item.get("Nr. quipam."),
            item.get("Marca / Modelo.1"),
            item.get("Ano.1"),
            item.get("Lt. Diesel.1"),
            item.get("Méd..1"),
            item.get("Méd..2"),
            item.get("LT / DIA"),
            item.get("KM RODADO"),
            item.get("DIF"),
            item.get("MEDIA"),
            item.get("DIF. MEDIA")
        ))


    conec.commit()
    cursor.close()

def obter_dados():
    con = conectar()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM DadosTelemetria")
    dados = cursor.fetchall()
    con.close()
    return dados

def placas_dados():
    con = conectar()
    cursor = con.cursor()
    cursor.execute("SELECT placa FROM DadosTelemetria;")
    dados = cursor.fetchall()
    con.close()
    
    # Extrair as placas como strings e colocar em maiúsculas
    return [linha[0].upper() for linha in dados]

def motorista_dados():
    con = conectar()
    cursor = con.cursor()
    cursor.execute(
        """
        SELECT 
            motorista, nr_acerto, data, data_saida, data_chegada,
            km_saida, km_chegada, km_rodado, km_vazio, porcento_vazio,
            qtd_dias, total_hrs, lt_diesel, media, lt_arla, 
            porcento_arla,lt_por_dia, km_rodado_dup, dif, media_dup, 
            dif_media
        FROM DadosTelemetria;
        """
    )
    dados_tuplas = cursor.fetchall()
    con.close()
    
    colunas = [
        "motorista", "nr_acerto", "data", "data_saida", "data_chegada",
        "km_saida", "km_chegada", "km_rodado", "km_vazio", "porcento_vazio",
        "qtd_dias", "total_hrs", "lt_diesel", "media", "lt_arla", "porcento_arla",
        "lt_por_dia", "km_rodado_dup", "dif", "media_dup", "dif_media"
    ]
    
    dados = [dict(zip(colunas, linha)) for linha in dados_tuplas]
    return dados

def veiculo_dados():
    
    con = conectar()
    cursor = con.cursor()
    cursor.execute(
        """
        SELECT 
            frota, 
            placa, 
            marca_modelo, 
            data,
            ano_veiculo,
            nr_equipamento, 
            marca_modelo_equipamento, 
            ano_equipamento,
            lt_diesel_equip, 
            media_1, 
            media_2,
            media,
            km_rodado_dup
        FROM DadosTelemetria;
        """
    )
    dados_tuplas = cursor.fetchall()
    con.close()

    colunas = [
        "frota", "placa", "marca_modelo", "data", "ano_veiculo",
        "nr_equipamento", "marca_modelo_equipamento", "ano_equipamento",
        "lt_diesel_equip", "media_1", "media_2", "media", "km_rodado_dup"
    ]

    dados = [dict(zip(colunas, linha)) for linha in dados_tuplas]
    return dados
    
    
    

def main():
    with open("dados_filtrados_2025.json", "r", encoding="utf-8") as f:
        dados_json = json.load(f)
    
    criar_tabela()
    inserir_dados(dados_json)

if __name__ == "__main__":
    main()