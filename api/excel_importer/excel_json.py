import pandas as pd


# Caminho do arquivo
arquivo = "./uploads/dados2.xlsm"
#'api/excel_importer/dados2.xlsm'
#arquivo = '/home/rafael/Documentos/Projetos/Projetos Feelancer/Projeto-Telemetria/api/excel_importer/dados2.xlsm'


# Lê a primeira aba (ou especifique o nome se souber)
df = pd.read_excel(arquivo, sheet_name=0, engine="openpyxl")

# Remove linhas onde 'Data' está vazio
df = df[df['Data'].notna()]

# Converte colunas de data
df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%y', errors='coerce')
df['Data de Saida'] = pd.to_datetime(df['Data de Saida'], format='%d/%m/%y %H:%M:', errors='coerce')
df['Data de Cheg.'] = pd.to_datetime(df['Data de Cheg.'], format='%d/%m/%y %H:%M:', errors='coerce')

# Filtra os dados a partir de 2025
df_filtrado = df[df['Data'].dt.year >= 2025]

# Remove colunas "Unnamed"
df_filtrado = df_filtrado.loc[:, ~df_filtrado.columns.str.contains('^Unnamed')]

# Formata datas para string no padrão dd/mm/yyyy
df_filtrado['Data'] = df_filtrado['Data'].dt.strftime('%d/%m/%Y')
df_filtrado['Data de Saida'] = df_filtrado['Data de Saida'].dt.strftime('%d/%m/%Y %H:%M')
df_filtrado['Data de Cheg.'] = df_filtrado['Data de Cheg.'].dt.strftime('%d/%m/%Y %H:%M')

# Exibe os dados
print(df_filtrado)

# Salva em JSON com datas formatadas
df_filtrado.to_json("dados_filtrados_2025.json", orient="records", indent=4, force_ascii=False)
    