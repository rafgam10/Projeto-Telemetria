import pandas as pd
from tabulate import tabulate

# Caminho para o arquivo .xlsm
caminho_arquivo = '/home/rafael/Documentos/Projetos/Projetos Feelancer/Projeto-Telemetria/api/excel_importer/dados2.xlsm'

# Carrega todos os dados da primeira aba
df = pd.read_excel(caminho_arquivo, engine='openpyxl')  # ou use engine='xlrd' se necessário

# Exibe as primeiras linhas para verificar
print(df.columns)

# jsonData = df.to_json("dados.json")