# Projeto-Telemetria


### 📁 Estrutura Geral do Projeto

```
projeto-telemetria/
├── api/                      # Backend (API REST)
│   ├── app.py               # Arquivo principal Flask
│   ├── requirements.txt     # Dependências da API
│   ├── models/              # Modelos de dados (Ex: Motorista, Desempenho)
│   ├── resources/           # Rotas e lógica dos endpoints da API
│   ├── database/            # Configuração do banco de dados (SQLite ou PostgreSQL)
│   └── excel_importer/      # Scripts para leitura automática da planilha Excel

├── mobile_app/              # Aplicativo Mobile feito com KivyMD
│   ├── main.py              # App principal
│   ├── screens/             # Telas (login, dashboard, histórico, etc.)
│   ├── services/            # Comunicação com a API (requisições HTTP)
│   └── assets/              # Ícones, fontes, imagens

├── docs/                    # Documentação do projeto
│   ├── wireframes/          # Rascunhos e fluxos das telas
│   └── README.md            # Explicação do projeto

└── .gitignore               # Ignorar arquivos sensíveis (como banco, tokens)
```

---

### ✅ Etapas do Projeto

1. **📊 Coleta de Dados (Excel)**
   - Automatizar leitura do Excel (pandas ou openpyxl).
   - Converter para dados estruturados (JSON ou banco de dados).
   - Rodar esse processo automaticamente (por exemplo, toda vez que o Excel for atualizado).

2. **🔌 API com Flask**
   - Endpoints REST:
     - `/login`
     - `/motorista/<id>`
     - `/motorista/<id>/desempenho`
     - `/api/placas` - O Caminho para os dados das placas.
   - Banco de dados relacional (SQLite para testes, PostgreSQL na produção).
   - Proteção com JWT para login e acesso seguro.

3. **📱 App com KivyMD**
   - Tela de login.
   - Dashboard com desempenho (gráficos e notas).
   - Tela de histórico com últimos dados.
   - Conexão com API via `requests`.

4. **🚀 Hospedagem**
   - API hospedada em Render, Fly.io ou outro serviço.
   - Se quiser evitar custos, pode hospedar localmente ou usar plano gratuito.



