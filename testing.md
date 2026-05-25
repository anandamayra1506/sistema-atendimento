# Plano de Testes: Sistema ResolveAí (Help Desk)
**Metodologia:** TDD First (Test-Driven Development)

## 1. Visão Geral e Estratégia
Conforme a metodologia TDD First, os testes automatizados deste plano devem ser escritos **antes** da implementação do código funcional. A estratégia visa garantir a integridade das especificações do sistema (RBAC e transições de status) e será executada através do framework `pytest`.

## 2. Cenários Críticos de Teste

### Funcionalidade 1: Controle de Acesso (RBAC)
* **Cenário Crítico:** Tentativa de escalonamento de privilégios.
* **Teste:** Validar se um usuário cadastrado como "cliente" consegue acessar a rota de criação de atendentes (`/admin/atendentes/novo`).
* **Ação TDD:** Escrever teste simulando requisição POST na rota restrita com credenciais de cliente.
* **Resultado Esperado:** O sistema deve rejeitar a requisição (Erro 403 Forbidden) e o banco de dados não deve sofrer alterações.

### Funcionalidade 2: Operação de Tickets (Chamados)
* **Cenário Crítico:** Transição de status obrigatória ("Aberto" para "Em Andamento").
* **Teste:** Garantir que a primeira resposta enviada por um perfil "atendente" altere automaticamente o status do ticket.
* **Ação TDD:** Inserir um ticket "Aberto" via fixture. Simular sessão de "atendente" e submeter resposta via POST em `/ticket/{id}`.
* **Resultado Esperado:** A resposta deve ser gravada e o atributo `status` do ticket deve atualizar para "Em Andamento".

### Funcionalidade 3: Avaliação de Qualidade
* **Cenário Crítico:** Avaliação prematura de um atendimento.
* **Teste:** Impedir que o sistema registre uma nota de satisfação para um ticket que não foi concluído.
* **Ação TDD:** Simular POST enviando nota de 1 a 5 estrelas para um ticket com status "Em Andamento".
* **Resultado Esperado:** O sistema deve ignorar o dado, mantendo o campo `nota` como NULO, e retornar erro de validação.

## 3. Utilização de Mocks
Para manter os testes unitários isolados, rápidos e determinísticos, utilizaremos as seguintes simulações (Mocks):
* **Mock de Banco de Dados:** Substituição do banco de dados em disco (`database.db`) por um banco temporário em memória (`sqlite:///:memory:`) injetado via Fixture do Pytest durante a execução da suíte.
* **Mock de Sessão e Rotas:** Utilização da biblioteca `pytest-flask` (`app.test_client()`) para simular chamadas HTTP e injetar usuários logados sem a necessidade de interagir com o navegador físico.

## 4. Prevenção de Regressões
A validação de alterações será automatizada. Qualquer nova modificação no código-fonte exigirá a execução do comando raiz `pytest`. A aprovação em 100% dos testes deste plano é requisito obrigatório para a consolidação de novas versões na branch `main`, evitando que futuras atualizações quebrem as regras de negócio já estabelecidas.

## 5. Testes de Interface (Frontend)
* **CT-FE-01 (Responsividade):** Simular o acesso ao Dashboard em resolução Mobile (360x640). A tabela de tickets não deve quebrar o layout, ativando a rolagem horizontal (`table-responsive`).
* **CT-FE-02 (Estado Vazio):** Acessar a tela inicial com uma conta recém-criada (sem chamados). O sistema deve exibir o alerta amigável de "Nenhum chamado encontrado" ao invés da estrutura vazia da tabela.
* **CT-FE-03 (Validação de Formulário):** Clicar no botão "Entrar" na tela de Login sem preencher os campos. O navegador deve reter a submissão e exibir o aviso nativo de "Preencha este campo" (`required`).