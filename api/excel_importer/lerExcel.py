import pandas as pd
from tabulate import tabulate

# # Caminho para o arquivo .xlsm
# #caminho_arquivo = '/home/rafael/Documentos/Projetos/Projetos Feelancer/Projeto-Telemetria/api/excel_importer/dados2.xlsm'
# caminho_arquivo = "./uploads/Resumo de operação do veículo.csv"
# # Carrega todos os dados da primeira aba
# df = pd.read_excel(caminho_arquivo, engine='openpyxl')  # ou use engine='xlrd' se necessário

# # Exibe as primeiras linhas para verificar
# print(df.columns)

# # jsonData = df.to_json("dados.json")

# Caminho para o arquivo CSV
#caminho_arquivo = "./uploads/Resumo de operação do veículo.csv"
caminho_arquivo = "/home/rafael/Documentos/Projetos/Projetos Feelancer/Projeto-Telemetria/api/uploads/Resumo de operação do motorista.csv"
# Carrega o arquivo CSV corretamente
df = pd.read_csv(caminho_arquivo)

# Exibe as colunas para verificação
print(df.columns)

# (Opcional) Salvar em JSON
# df.to_json("dados.json", orient='records', force_ascii=False)