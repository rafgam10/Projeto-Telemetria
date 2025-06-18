
# 🚛 Projeto de Análise de Telemetria Veicular

Este projeto foi desenvolvido para uma empresa focada em **análise de dados de telemetria**, com o objetivo de automatizar a coleta, estruturação e visualização de informações sobre motoristas e veículos. O sistema possibilita controle detalhado sobre consumo, desempenho, metas operacionais e rankings.

---

## 🧠 Tecnologias Utilizadas

- **Python** (backend)
- **Flask** (framework web)
- **MySQL** (banco de dados relacional)
- **Pandas & Openpyxl** (leitura e processamento de planilhas)
- **HTML/CSS + Tailwind** (interface de administração)
- **JavaScript** (interações dinâmicas)
- **Jinja2** (templates Flask)
- **Bootstrap Icons / Phosphor Icons** (ícones da UI)

---

## 📁 Estrutura Geral do Projeto

```
projeto-telemetria/
├── api/
│   ├── app.py                  # Arquivo principal Flask
│   ├── requirements.txt        # Dependências
│   ├── views/                  # Rotas (admin e usuário)
│   ├── database/               # Conexão e scripts SQL
│   └── excel_importer/         # Importação de dados via planilha Excel
├── templates/                  # Páginas HTML com Jinja2
├── static/                     # Estilos, imagens e scripts JS
└── uploads/                    # Planilhas temporárias importadas
```

---

## 🔧 Funcionalidades Implementadas

### 📥 Importação de Planilhas
- Leitura automática de arquivos `.xlsx` com dados de veículos e motoristas.
- Extração e normalização dos dados.
- Inserção segura no banco de dados.
- Cálculo automático de notas de desempenho.

### 🔎 Gestão de Dados (Admin)
- Cadastro e visualização de empresas.
- Controle de motoristas e veículos por empresa.
- Registro de auditoria e segurança via sessão Flask.
- Ranking com os 5 melhores motoristas (baseado em metas de consumo e eficiência).

### 🎯 Metas de Consumo
- Criação de metas por modelo de veículo.
- Comparação automática entre o consumo real e a meta.
- Reavaliação das notas dos motoristas com base na performance.

---

## 🏁 Como Rodar Localmente

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/projeto-telemetria.git
   cd projeto-telemetria/api
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure o banco de dados MySQL:
   - Execute os scripts SQL em `database/` para criar as tabelas.
   - Altere as configurações de conexão em `database_config.py`.

4. Execute o servidor:
   ```bash
   python app.py
   ```

---

## ✅ Status do Projeto

✔️ Finalizado para entrega em ambiente corporativo.  
📦 Extensível para dashboard com gráficos e notificações futuras.

---

## 📌 Observações

Este projeto é ideal para empresas que desejam otimizar a análise de dados operacionais de frota, associando métricas de desempenho com avaliação de condutores e veículos.

---

## 🧾 Licença

Distribuído sob licença MIT. Consulte `LICENSE` para mais informações.
```
