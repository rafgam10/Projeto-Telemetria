import sqlite3
import json

NOMETABELA = "DadosTelemetria"

def conectar():
    return sqlite3.connect(f"api/database/{NOMETABELA}.db")


def criar_tabela():
    conec = conectar()
    cursor = conec.cursor()

    sql = f"""
        CREATE TABLE IF NOT EXISTS {NOMETABELA}(
            
            motorista TEXT,

            placa TEXT,
            frota TEXT,
            marca TEXT,

            data TEXT,
            datasSaida TEXT,
            dataChegada TEXT,
            qtdDias INTEGER,
            totalHrs INTEGER,

            KmSaida INTEGER,
            KmChegada INTEGER,
            KmRodado INTEGER,

            LtArla REAL,
            LtDiesel REAL,
            LtPorDia REAL


        )
    """

    cursor.execute(sql)

    conec.commit()
    cursor.close()

def inserir_dados(dados):
    conec = conectar()
    cursor = conec.cursor()

    for item in dados:
        cursor.execute(f"""
            INSERT INTO {NOMETABELA} (
                motorista, placa, frota, marca, data, datasSaida, dataChegada,
                qtdDias, totalHrs, KmSaida, KmChegada, KmRodado,
                LtArla, LtDiesel, LtPorDia
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            item.get("MOTORISTA"),
            item.get("Placa"),
            item.get("Frota"),
            item.get("Marca / Modelo"),
            item.get("Data"),
            item.get("Data de Saida"),
            item.get("Data de Cheg."),
            item.get("Qtd Dias"),
            item.get("Tot. Hrs"),
            item.get("Km Saída"),
            item.get("Km Cheg."),
            item.get("Km Rod."),
            item.get("Lt. Arla"),
            item.get("Lt. Diesel"),
            item.get("LT / DIA")
        ))

    conec.commit()
    cursor.close()

def obter_dados():
    conec = conectar()
    cursor = conec.cursor()

    cursor.execute(f"SELECT * FROM {NOMETABELA}")
    dados = cursor.fetchall()
    conec.close()

    return dados

def main():
    with open("dados_filtrados_2025.json", "r", encoding="utf-8") as f:
        dados_json = json.load(f)
    
    criar_tabela()
    inserir_dados(dados_json)

if __name__ == "__main__":
    main()