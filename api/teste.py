import sqlite3
import pandas as pd
from faker import Faker 
import random
from datetime import datetime, timedelta

def criar_banco(nome_arquivo='telemetria.db'):
    conexao = sqlite3.connect(f"api/database/{nome_arquivo}")
    cursor = conexao.cursor()

    # Comandos SQL para criação das tabelas
    script_sql = """
        CREATE TABLE IF NOT EXISTS Empresas (
        id_empresa INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_empresa TEXT NOT NULL,
        cnpj TEXT UNIQUE NOT NULL
    );

    CREATE TABLE IF NOT EXISTS Usuarios (
        id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
        id_empresa INTEGER NOT NULL,
        nome TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        senha_hash TEXT NOT NULL,
        tipo TEXT CHECK(tipo IN ('admin', 'motorista')) NOT NULL,
        FOREIGN KEY (id_empresa) REFERENCES Empresas(id_empresa)
    );

    CREATE TABLE IF NOT EXISTS Motoristas (
        id_motorista INTEGER PRIMARY KEY AUTOINCREMENT,
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
        id_veiculo INTEGER PRIMARY KEY AUTOINCREMENT,
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
        id_telemetria INTEGER PRIMARY KEY AUTOINCREMENT,
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
        id_log INTEGER PRIMARY KEY AUTOINCREMENT,
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


# criar_banco()

# Populando Empresas
faker = Faker("pt_BR")
empresas = [(1, "TransLogística Ltda", "12.345.678/0001-90"), (2, "ViaCargas Transportes", "98.765.432/0001-10")]
conn = sqlite3.connect("api/database/telemetria.db")
cursor = conn.cursor()
cursor.executemany("INSERT OR IGNORE INTO Empresas (id_empresa, nome_empresa, cnpj) VALUES (?, ?, ?);", empresas)

# Populando Motoristas e Veículos
motoristas = []
veiculos = []
dados_telemetria = []

for i in range(1, 21):
    id_empresa = random.choice([1, 2])
    nome_motorista = faker.name()
    motorista = (
        i, id_empresa, nome_motorista, faker.cpf(), faker.bothify(text="###########"), 
        faker.date_of_birth(minimum_age=25, maximum_age=60).isoformat(), 
        round(random.uniform(3.0, 5.0), 1), 
        random.choice(["Ativo", "Inativo"])
    )
    motoristas.append(motorista)

    modelo = random.choice(["FH 460", "R 450", "Axor 2544"])
    marca = random.choice(["Volvo", "Scania", "Mercedes-Benz"])
    placa = faker.license_plate()
    km_atual = round(random.uniform(10000, 200000), 2)
    veiculo = (
        i, id_empresa, placa, modelo, marca, random.randint(2015, 2023), 
        str(random.randint(1000, 4000)), km_atual, round(random.uniform(2.0, 4.5), 2),
        (datetime.now() - timedelta(days=random.randint(10, 180))).date().isoformat(),
        random.choice(["Disponível", "Indisponível", "Em Manutenção"])
    )
    veiculos.append(veiculo)

    data_saida = datetime.now() - timedelta(days=random.randint(1, 30))
    dias = random.randint(1, 5)
    data_chegada = data_saida + timedelta(days=dias)
    hodometro_inicial = round(km_atual - random.uniform(500, 2000), 2)
    hodometro_final = km_atual
    km_rodado = hodometro_final - hodometro_inicial
    km_vazio = round(km_rodado * random.uniform(0.05, 0.25), 2)
    porcento_vazio = round((km_vazio / km_rodado) * 100, 2)
    velocidade_media = round(random.uniform(20.0, 80.0), 2)
    rotacao_maxima = random.randint(1800, 3500)
    consumo_diesel = round(random.uniform(25.0, 45.0), 2)
    consumo_arla = round(random.uniform(1.0, 5.0), 2)
    marcha_lenta = f"{random.randint(1,3)}h{random.randint(0,59)}min"
    total_hrs = dias * 24
    media_km_l = round(km_rodado / (consumo_diesel/100*km_rodado), 2)
    lt_diesel_total = round((consumo_diesel/100)*km_rodado, 2)
    lt_arla_total = round((consumo_arla/100)*km_rodado, 2)
    lt_por_dia = round(lt_diesel_total / dias, 2)
    km_rodado_dup = km_rodado + random.uniform(-10, 10)
    dif_km = km_rodado_dup - km_rodado
    media_dup = round(km_rodado_dup / (lt_diesel_total if lt_diesel_total else 1), 2)
    dif_media = media_dup - media_km_l

    dados_telemetria.append((
        i, id_empresa, i, i, data_saida.isoformat(), data_chegada.isoformat(),
        hodometro_inicial, hodometro_final, km_rodado, km_vazio, porcento_vazio,
        velocidade_media, rotacao_maxima, consumo_diesel, consumo_arla, marcha_lenta,
        dias, total_hrs, media_km_l, lt_diesel_total, lt_arla_total, lt_por_dia,
        km_rodado_dup, dif_km, media_dup, dif_media, datetime.now().isoformat()
    ))

cursor.executemany("INSERT OR IGNORE INTO Motoristas VALUES (?, ?, ?, ?, ?, ?, ?, ?);", motoristas)
cursor.executemany("INSERT OR IGNORE INTO Veiculos VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", veiculos)
cursor.executemany("INSERT INTO DadosTelemetria VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", dados_telemetria)

conn.commit()
conn.close()
