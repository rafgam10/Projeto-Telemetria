import pandas as pd

# Caminho do arquivo
arquivo = '/home/rafael/Documentos/Projetos/Projetos Feelancer/Projeto-Telemetria/api/excel_importer/dados2.xlsm'

# Lê a primeira aba (ou especifique o nome se souber)
df = pd.read_excel(arquivo, sheet_name=0)

# Remove linhas onde 'Data' está vazio
df = df[df['Data'].notna()]

# Converte a coluna 'Data' para datetime (ex: 23/01/25)
df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%y', errors='coerce')

# Filtra os dados a partir de 2025
df_filtrado = df[df['Data'].dt.year >= 2025]

#Colunas "Unnamed" serão excluídas se contiverem valores 
df_filtrado = df_filtrado.loc[:, ~df_filtrado.columns.str.contains('^Unnamed')]

# Exibe os dados ou salva
print(df_filtrado)

# Opcional: salvar como JSON
df_filtrado.to_json("dados_filtrados_2025.json", orient="records", indent=4, force_ascii=False)
