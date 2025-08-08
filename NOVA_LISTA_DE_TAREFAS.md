
- [X] - mudar nome da rota de logs para "metas";
- [X] - Alterar o nome do arquivo html "logs" para o novo "metas";

- [X] - trocar todos o L/100km por Km/Litro `(trocado alguns)`

- [ ] - rotas para adm:
	* [x] - de consumo semanal de diesel - `(modifiquei e testei)`
	* [X] - de motorista retorna todas as info de motorista - `views/api/routas.py -> motorista_info`
	* [X] - de veiculo retorna todas as info de veiculo - `views/api/routes.py -> veiculo_info`
	* [X] - de relatorio e estatistica, vê isso ai direito. `Feito e testado`
	* [X] - de metas de consumo dps. `AN - OBJ`
	* [X] - Exibir a avaliação do motorista `colocar na página gestão motorista.`

- [X] - rotas para user:
	* [X] - de distancia percorrida a cada semana - `views/api/routas.py -> distancia_semanal`  
	* [X] - de média de distancia percorrida a cada semana por forta (pega todas da mesma frota e faz média) - `views/api/routes.py -> media_semanal_frota`
	* [X] - de soma de km rodado (soma cada semana e reseta a cada mes) - `views/api/routes.py -> soma_km_semanal`
	* [X] - de informações do usuário - `views/user/routes.py -> pagina_user, pagina_perfil / Dados - database/user_database/user.py -> user_dados, perfil_user`;
	* [X] - de informações do veículo - `views/api/routes.py -> veiculo_info`

- [X] - AJUSTAR LOGIN DE USUÁRIO.

- [X] - REVER ROTAS DE API (tem algumas que tão no sqlite ainda e algumas que não vao ser usadas) `arrumei algumas, mas ainda tem oq arrumar`
- [X] - REFAZER BANCO DE DADOS NOVAMENTE COM AVALIAÇÃO
- [X] - FAZER NOVO GRAFICO DE COSUMO SEMANAL (GRAFICO HOME ADMIN)
- [ ] - Revisar as Rotas de API e do Projeto todo, para verificação.

- [X] - sistema de rankeamento

- [X] - aceitar importações de dois arquivos exel separados (motorista e vículo):
	* [X] - Mandar o arquivo excel primeiro na pasta uploads.
	* [X] - Extrair dados pela pastas uploads e mandar para o DB.
	* [X] - Deletar o arquivo excel na pasta uploads.
	* [X] - Fazer a verificação.

- ADMIN ROUTES ESTÁ A ROTA DE ALTERAR O BANCO DE METAS

- [-] - gerar apk webview

- Modificações/Tarefas Futuras dia 13/julho
	* [X] - Criação da rota de painel de empresas.
	* [X] - Criar a lógica de GET, DELETE e PUT/POST de cada empresa.
	* [X] - Criar Tabela para informar datas e itens de cada importação.
	* [X] - Criar a rota para exibir datas de importação.
	* [X] - Criar os logs de cada registros dos dados de importação feito.
	* [X] - Deletar registro de importações e todos os dados relacionados.

- Melhorias Futuras:
	* [ ] - Separação dos logins, tanto por users e por admins.
	* [ ] - Fazer tratamento de erros, para buscar bugs mais rápido.
	* [ ] - Melhorar a filtagens dos dados na importação.
	* [ ] - Fazer validações em alguns trechos de códigos.

`Task Final:`
# - [X] - Limpar o repo do GitHub.
# - [ ] - Escrever uma documentação do Projeto.