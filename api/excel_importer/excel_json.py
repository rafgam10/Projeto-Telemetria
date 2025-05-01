import pandas as pd

# Caminho do arquivo
arquivo = '/home/rafael/Documentos/Projetos/Projetos Feelancer/Projeto-Telemetria/api/excel_importer/dados2.xlsm'

# Carregar o Excel
df = pd.read_excel(arquivo, sheet_name=0, engine="openpyxl")

# Converter a coluna de data para datetime
df['Data inicial da operação'] = pd.to_datetime(df['Data inicial da operação'], errors='coerce')

# Filtrar apenas registros com ano >= 2025
df_filtrado = df[df['Data inicial da operação'].dt.year >= 2025]

# Visualizar os dados filtrados
print(df_filtrado)

# (Opcional) Exportar para JSON
df_filtrado.to_json("dados_filtrados_2025.json", orient="records", indent=4, force_ascii=False)
