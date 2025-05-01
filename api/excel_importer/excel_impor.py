import pandas as pd
import sqlite3
import os
import re

# Caminho do arquivo Excel
arquivo_excel = "dados2.xlsm"

# Caminho onde o banco SQLite será salvo
caminho_banco = "telemetria.db"  # Exemplo: salvar no diretório atual do script

# # Cria a pasta se não existir
# os.makedirs(os.path.dirname(caminho_banco), exist_ok=True)

# Conecta (ou cria) o banco
conexao = sqlite3.connect(caminho_banco)

# Lê todas as abas
xls = pd.ExcelFile(arquivo_excel, engine='openpyxl')
abas = xls.sheet_names

for aba in abas:
    print(f"Importando aba: {aba}")

    try:
        # Lê a aba
        df = pd.read_excel(xls, sheet_name=aba)

        # Limpa o nome da aba para usar como nome de tabela
        nome_tabela = re.sub(r'\W+', '_', aba.strip().lower())

        # Exporta para SQLite
        df.to_sql(nome_tabela, conexao, if_exists='replace', index=False)
        print(f"✅ Tabela '{nome_tabela}' criada com sucesso.")
    except Exception as e:
        print(f"❌ Erro ao importar aba '{aba}': {e}")

conexao.close()
print("\n✅ Todas as abas foram processadas e importadas.")
