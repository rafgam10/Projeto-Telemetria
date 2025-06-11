import pandas as pd
from tabulate import tabulate

# Caminho para o arquivo
caminho_arquivo = "/home/rafael/Documentos/Projetos/Projetos Feelancer/Projeto-Telemetria/uploads/base 3.xlsx"

# Lê o Excel, pulando as 2 primeiras linhas
df = pd.read_excel(caminho_arquivo, engine="openpyxl", skiprows=2)

# Remove possíveis linhas completamente vazias
df = df.dropna(how='all')

# Exibe as colunas reais
print("Colunas reais detectadas:")
print(df.columns)

# Exibe as 5 primeiras linhas formatadas
print(tabulate(df.head(), headers='keys', tablefmt='psql'))
