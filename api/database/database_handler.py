import sqlite3
import json
from datetime import datetime

NOMETABELA = "telemetria.db"

def conectar():
    return sqlite3.connect(f'api/database/{NOMETABELA}')
    #return sqlite3.connect(f"api/database/{NOMETABELA}.db")


# def criar_tabela():
#     conec = conectar()
#     cursor = conec.cursor()
#     cursor.execute(f"DROP TABLE IF EXISTS {NOMETABELA}")
#     cursor.execute(f"""
#         CREATE TABLE IF NOT EXISTS {NOMETABELA} (
#             motorista TEXT,
#             nr_acerto INTEGER,
#             data TEXT,
#             data_saida TEXT,
#             data_chegada TEXT,
#             km_saida REAL,
#             km_chegada REAL,
#             km_rodado REAL,
#             km_vazio REAL,
#             porcento_vazio REAL,
#             qtd_dias INTEGER,
#             total_hrs INTEGER,
#             frota TEXT,
#             placa TEXT,
#             marca_modelo TEXT,
#             ano_veiculo INTEGER,
#             lt_diesel REAL,
#             media REAL,
#             lt_arla REAL,
#             porcento_arla REAL,
#             nr_equipamento INTEGER,
#             marca_modelo_equipamento TEXT,
#             ano_equipamento INTEGER,
#             lt_diesel_equip REAL,
#             media_1 REAL,
#             media_2 REAL,
#             lt_por_dia REAL,
#             km_rodado_dup REAL,
#             dif REAL,
#             media_dup REAL,
#             dif_media REAL
#         )
#     """)

#     # cursor.execute(sql)

#     conec.commit()
#     cursor.close()


def criar_banco(nome_arquivo='telemetria.db'):
    conexao = sqlite3.connect(nome_arquivo)
    cursor = conexao.cursor()

    # Comandos SQL para criação das tabelas
    script_sql = """
    CREATE TABLE IF NOT EXISTS Empresas (
        id_empresa INTEGER PRIMARY KEY,
        nome_empresa TEXT NOT NULL,
        cnpj TEXT UNIQUE NOT NULL
    );

    CREATE TABLE IF NOT EXISTS Usuarios (
        id_usuario INTEGER PRIMARY KEY,
        id_empresa INTEGER NOT NULL,
        nome TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        senha_hash TEXT NOT NULL,
        tipo TEXT CHECK(tipo IN ('admin', 'motorista')) NOT NULL,
        FOREIGN KEY (id_empresa) REFERENCES Empresas(id_empresa)
    );

    CREATE TABLE IF NOT EXISTS Motoristas (
        id_motorista INTEGER PRIMARY KEY,
        id_empresa INTEGER NOT NULL,
        nome TEXT NOT NULL,
        cpf TEXT UNIQUE NOT NULL,
        cnh TEXT NOT NULL,
        data_nascimento TEXT,
        avaliacao REAL,
        status TEXT CHECK(status IN ('Ativo', 'Inativo')) DEFAULT 'Ativo',
        FOREIGN KEY (id_empresa) REFERENCES Empresas(id_empresa)
    );

    CREATE TABLE IF NOT EXISTS Veiculos (
        id_veiculo INTEGER PRIMARY KEY,
        id_empresa INTEGER NOT NULL,
        placa TEXT UNIQUE NOT NULL,
        modelo TEXT NOT NULL,
        marca TEXT NOT NULL,
        ano INTEGER,
        frota TEXT,
        km_atual REAL,
        media_km_litro REAL,
        ultima_manutencao TEXT,
        status TEXT CHECK(status IN ('Disponível', 'Indisponível', 'Em Manutenção')) DEFAULT 'Disponível',
        FOREIGN KEY (id_empresa) REFERENCES Empresas(id_empresa)
    );

    CREATE TABLE IF NOT EXISTS DadosTelemetria (
        id_telemetria INTEGER PRIMARY KEY,
        id_empresa INTEGER NOT NULL,
        id_motorista INTEGER NOT NULL,
        id_veiculo INTEGER NOT NULL,
        data_saida TEXT NOT NULL,
        data_chegada TEXT NOT NULL,
        hodometro_inicial REAL,
        hodometro_final REAL,
        km_rodado REAL,
        km_vazio REAL,
        porcento_vazio REAL,
        velocidade_media REAL,
        rotacao_maxima INTEGER,
        consumo_diesel REAL,
        consumo_arla REAL,
        marcha_lenta TEXT,
        total_dias INTEGER,
        total_hrs INTEGER,
        media_km_l REAL,
        lt_diesel_total REAL,
        lt_arla_total REAL,
        lt_por_dia REAL,
        km_rodado_dup REAL,
        dif_km REAL,
        media_dup REAL,
        dif_media REAL,
        data_registro TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (id_empresa) REFERENCES Empresas(id_empresa),
        FOREIGN KEY (id_motorista) REFERENCES Motoristas(id_motorista),
        FOREIGN KEY (id_veiculo) REFERENCES Veiculos(id_veiculo)
    );

    CREATE TABLE IF NOT EXISTS LogsAuditoria (
        id_log INTEGER PRIMARY KEY,
        id_empresa INTEGER NOT NULL,
        usuario TEXT NOT NULL,
        acao TEXT NOT NULL,
        tabela_afetada TEXT,
        data_hora TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (id_empresa) REFERENCES Empresas(id_empresa)
    );
    """

    cursor.executescript(script_sql)
    conexao.commit()
    conexao.close()
    print("Banco de dados e tabelas criados com sucesso.")


# Inserir empresas novamente agora que a tabela existe
def inserir_empresas(dados):
    conexao = conectar()
    cursor = conexao.cursor()
    
    empresas = [
        ("TransLog Transportes", "12.345.678/0001-90"),
        ("Rodovia Express", "98.765.432/0001-21")
    ]
    
    cursor.executemany("""
        INSERT INTO Empresas (nome_empresa, cnpj) 
        VALUES (?, ?)
    """, empresas)
    
    conexao.commit()
    conexao.close()

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
            motorista,
            frota, 
            placa, 
            marca_modelo, 
            data,
            ano_veiculo,
            nr_equipamento, 
            marca_modelo_equipamento, 
            ano_equipamento,
            lt_diesel,
            lt_arla,
            lt_diesel_equip, 
            media_1, 
            media_2,
            media,
            data_chegada,
            km_rodado_dup
            
        FROM DadosTelemetria;
        """
    )
    dados_tuplas = cursor.fetchall()
    con.close()
    
    colunas = [
        "motorista","frota", "placa", "marca_modelo", "data", "ano_veiculo",
        "nr_equipamento", "marca_modelo_equipamento", "ano_equipamento",
        "lt_diesel", "lt_arla", "lt_diesel_equip", "media_1", "media_2", "media", "data_chegada",
        "km_rodado_dup"
    ]
    
    dados = [dict(zip(colunas, linha)) for linha in dados_tuplas]
    
    
    for motorista in dados:
        try:
            idMotorista_nomeMotorista = str(motorista['motorista']).split(" - ")
            motorista["id_motorista"] = idMotorista_nomeMotorista[0].strip()
            motorista["nome_motorista"] = idMotorista_nomeMotorista[1].strip()
            km = float(motorista["km_rodado_dup"])
            diesel = float(motorista["lt_diesel"])
            arla = float(motorista["lt_arla"])

            if km > 0:
                motorista["lt_diesel"] = round((diesel / km) * 100, 2)
                motorista["lt_arla"] = round((arla / km) * 100, 2)
            else:
                motorista["lt_diesel"] = 0
                motorista["lt_arla"] = 0
        except (ValueError, ZeroDivisionError, TypeError):
            motorista["lt_diesel"] = 0
            motorista["lt_arla"] = 0

    return dados


############################### pra aparecer só um motora ###############


def motorista_dados_unicos():
    con = conectar()
    cursor = con.cursor()
    cursor.execute(
        """
        SELECT 
            motorista,
            frota, 
            placa, 
            marca_modelo, 
            data,
            ano_veiculo,
            nr_equipamento, 
            marca_modelo_equipamento, 
            ano_equipamento,
            lt_diesel,
            lt_arla,
            lt_diesel_equip, 
            media_1, 
            media_2,
            media,
            data_chegada,
            km_rodado_dup
        FROM DadosTelemetria;
        """
    )
    dados_tuplas = cursor.fetchall()
    con.close()

    colunas = [
        "motorista", "frota", "placa", "marca_modelo", "data", "ano_veiculo",
        "nr_equipamento", "marca_modelo_equipamento", "ano_equipamento",
        "lt_diesel", "lt_arla", "lt_diesel_equip", "media_1", "media_2", "media", "data_chegada",
        "km_rodado_dup"
    ]
    
    dados = [dict(zip(colunas, linha)) for linha in dados_tuplas]

    # ✅ Pegar apenas a viagem mais recente de cada motorista
    motoristas_unicos = {}
    for m in dados:
        try:
            id_nome = str(m["motorista"]).strip()
            data_str = m.get("data_chegada")
            data_formatada = datetime.strptime(data_str, "%d/%m/%Y %H:%M")
        except Exception:
            continue  # ignora linhas com erro

        if id_nome not in motoristas_unicos or data_formatada > motoristas_unicos[id_nome]["_data"]:
            m["_data"] = data_formatada
            motoristas_unicos[id_nome] = m

    dados_filtrados = list(motoristas_unicos.values())

    # ✅ Processar diesel/arla e separar ID e nome
    for motorista in dados_filtrados:
        try:
            idMotorista_nomeMotorista = str(motorista['motorista']).split(" - ")
            motorista["id_motorista"] = idMotorista_nomeMotorista[0].strip()
            motorista["nome_motorista"] = idMotorista_nomeMotorista[1].strip()
        except:
            motorista["id_motorista"] = ""
            motorista["nome_motorista"] = motorista["motorista"]

        try:
            km = float(motorista["km_rodado_dup"])
            diesel = float(motorista["lt_diesel"])
            arla = float(motorista["lt_arla"])

            if km > 0:
                motorista["lt_diesel"] = round((diesel / km) * 100, 2)
                motorista["lt_arla"] = round((arla / km) * 100, 2)
            else:
                motorista["lt_diesel"] = 0
                motorista["lt_arla"] = 0
        except (ValueError, ZeroDivisionError, TypeError):
            motorista["lt_diesel"] = 0
            motorista["lt_arla"] = 0

        del motorista["_data"]  # remover campo temporário

    return dados_filtrados


def veiculo_dados():
    
    con = conectar()
    cursor = con.cursor()
    cursor.execute(
        """
        SELECT 
            frota, 
            placa, 
            marca_modelo, 
            ano_veiculo,
            nr_equipamento, 
            marca_modelo_equipamento, 
            ano_equipamento,
            lt_diesel_equip, 
            media_1, 
            media_2,
            media,
            km_rodado_dup,
            data
        FROM DadosTelemetria;
        """
    )
    dados_tuplas = cursor.fetchall()
    con.close()

    colunas = [
        "frota", "placa", "marca_modelo", "ano_veiculo",
        "nr_equipamento", "marca_modelo_equipamento", "ano_equipamento",
        "lt_diesel_equip", "media_1", "media_2", "media", "km_rodado_dup", "data"]

    dados = [dict(zip(colunas, linha)) for linha in dados_tuplas]
    
    for veiculos in dados:
        try:
            marcaVeiculo_modeloVeiculo = str(veiculos['marca_modelo']).split(" / ")
            veiculos["marca_veiculo"] = marcaVeiculo_modeloVeiculo[0].strip()
            veiculos["modelo_veiculo"] = marcaVeiculo_modeloVeiculo[1].strip()

    
        except (ValueError, ZeroDivisionError, TypeError):
            pass
    
    return dados    


############################### pra aparecer só um veiculo ###############

def veiculo_dados_unicos():
    con = conectar()
    cursor = con.cursor()
    cursor.execute(
        """
        SELECT 
            frota, 
            placa, 
            marca_modelo, 
            ano_veiculo,
            nr_equipamento, 
            marca_modelo_equipamento, 
            ano_equipamento,
            lt_diesel_equip, 
            media_1, 
            media_2,
            media,
            km_rodado_dup,
            data
        FROM DadosTelemetria;
        """
    )
    dados_tuplas = cursor.fetchall()
    con.close()

    colunas = [
        "frota", "placa", "marca_modelo", "ano_veiculo",
        "nr_equipamento", "marca_modelo_equipamento", "ano_equipamento",
        "lt_diesel_equip", "media_1", "media_2", "media", "km_rodado_dup", "data"
    ]

    dados = [dict(zip(colunas, linha)) for linha in dados_tuplas]

    # ✅ Agrupar por placa e manter só o registro com data mais recente
    veiculos_unicos = {}
    for v in dados:
        try:
            placa = v["placa"].strip()
            data_str = v.get("data")
            data_formatada = datetime.strptime(data_str, "%d/%m/%Y")
        except Exception:
            continue

        if placa not in veiculos_unicos or data_formatada > veiculos_unicos[placa]["_data"]:
            v["_data"] = data_formatada
            veiculos_unicos[placa] = v

    dados_filtrados = list(veiculos_unicos.values())

    # ✅ Dividir marca/modelo
    for veiculo in dados_filtrados:
        try:
            marcaVeiculo_modeloVeiculo = str(veiculo['marca_modelo']).split(" / ")
            veiculo["marca_veiculo"] = marcaVeiculo_modeloVeiculo[0].strip()
            veiculo["modelo_veiculo"] = marcaVeiculo_modeloVeiculo[1].strip()
        except (ValueError, ZeroDivisionError, TypeError):
            veiculo["marca_veiculo"] = veiculo["marca_modelo"]
            veiculo["modelo_veiculo"] = ""

        del veiculo["_data"]  # remove campo temporário

    return dados_filtrados


    
def user_dados(placa):
    con = conectar()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM DadosTelemetria WHERE placa = ?", (placa,))
    dados_tuplas = cursor.fetchall()

    colunas = [
        "motorista", "nr_acerto", "data", "data_saida", "data_chegada",
        "km_saida", "km_chegada", "km_rodado", "km_vazio", "porcento_vazio",
        "qtd_dias", "total_hrs", "frota", "placa", "marca_modelo", "ano_veiculo",
        "lt_diesel", "media", "lt_arla", "porcento_arla",
        "nr_equipamento", "marca_modelo_equipamento", "ano_equipamento",
        "lt_diesel_equip", "media_1", "media_2",
        "lt_por_dia", "km_rodado_dup", "dif", "media_dup", "dif_media"
    ]

    dados_dict = [dict(zip(colunas, linha)) for linha in dados_tuplas]
    
    con.close()
    return dados_dict


def dados_por_id_motorista(id_motorista):
    con = conectar()
    cursor = con.cursor()

    # Converte tudo para maiúsculo para garantir a correspondência
    id_motorista = id_motorista.upper().strip() + '%'

    # Busca todos os registros onde o campo "motorista" começa com o ID informado
    cursor.execute("SELECT * FROM DadosTelemetria WHERE UPPER(motorista) LIKE ?", (id_motorista,))
    dados_tuplas = cursor.fetchall()

    colunas = [
        "motorista", "nr_acerto", "data", "data_saida", "data_chegada",
        "km_saida", "km_chegada", "km_rodado", "km_vazio", "porcento_vazio",
        "qtd_dias", "total_hrs", "frota", "placa", "marca_modelo", "ano_veiculo",
        "lt_diesel", "media", "lt_arla", "porcento_arla",
        "nr_equipamento", "marca_modelo_equipamento", "ano_equipamento",
        "lt_diesel_equip", "media_1", "media_2",
        "lt_por_dia", "km_rodado_dup", "dif", "media_dup", "dif_media"
    ]

    dados_dict = [dict(zip(colunas, linha)) for linha in dados_tuplas]
    
    con.close()
    return dados_dict


def dados_relatorios():
    con = conectar()
    cursor = con.cursor()

    # Buscar o último registro (por data mais recente) de cada motorista
    cursor.execute("""
        SELECT motorista, placa, MAX(data) as ultima_data
        FROM DadosTelemetria
        GROUP BY motorista, placa
    """)
    motoristas = cursor.fetchall()
    con.close()

    # Processar dados no formato (id, nome, placa)
    lista_motoristas = []
    for m in motoristas:
        try:
            id_nome = str(m[0]).split(" - ")  # Ex: "23 - João da Silva"
            id_motorista = id_nome[0].strip()
            nome_motorista = id_nome[1].strip()
            placa = m[1]
            lista_motoristas.append({
                "id": id_motorista,
                "nome": nome_motorista,
                "placa": placa
            })
        except Exception as e:
            print("Erro ao processar motorista:", e)
        
    return lista_motoristas

#================== Funções de Edição =================


    

def main():
    with open("dados_filtrados_2025.json", "r", encoding="utf-8") as f:
        dados_json = json.load(f)
    
    criar_tabela()
    inserir_dados(dados_json)

if __name__ == "__main__":
    main()