# Especificações do Sistema - ResolveAí (Help Desk)

## 1. Visão Geral
O ResolveAí é um sistema web projetado para centralizar o suporte e atendimento. Ele permite que clientes abram chamados (tickets) e interajam com a equipe técnica, enquanto gestores acompanham o volume de operações.

## 2. Regras de Negócio e Controle de Acesso (RBAC)
O sistema possui três níveis estritos de acesso:
* **Administrador (Proprietário):** Acesso total. Único perfil com permissão para cadastrar novos 'Atendentes' e visualizar o Dashboard Gerencial.
* **Atendente:** Acesso à fila global de atendimentos. Permissão para responder e alterar o status dos tickets.
* **Cliente:** Pode abrir novos chamados, interagir nos próprios chamados e encerrá-los.

## 3. Fluxo de Chamados (Tickets)
* **Aberto:** Status inicial de todo novo ticket criado pelo cliente.
* **Em Andamento:** Transição automática assim que um Atendente envia a primeira resposta.
* **Resolvido:** Status final. Apenas neste status o cliente tem a permissão de avaliar o atendimento com uma nota de 1 a 5 estrelas.

## 4. Modelos de Dados Principais
* **User:** id, nome, email, senha (hash), tipo (admin, atendente, cliente).
* **Ticket:** id, titulo, descricao, status, data_criacao, nota, cliente_id.
* **Reply (Resposta):** id, texto, data_resposta, ticket_id, autor_id.

## 5. Requisitos Técnicos
* **Backend:** Python 3.10+ com micro-framework Flask.
* **Banco de Dados:** SQLite, manipulado via ORM (Flask-SQLAlchemy).
* **Autenticação:** Gerenciamento de sessão via Flask-Login.

## 6. Otimizações de Desempenho e Arquitetura (Refatoração)
Para garantir a escalabilidade do sistema ResolveAí e o alto desempenho computacional, a arquitetura foi otimizada com:
* **Camada de Cache:** Utilização da biblioteca `Flask-Caching` para armazenar resultados de relatórios pesados (Dashboard). Isso reduz a carga de I/O no banco de dados durante picos de acesso.
* **Processamento Assíncrono (Jobs e Filas):** Separação de rotinas web das rotinas em segundo plano. O processamento de disparos sistêmicos (como notificações de encerramento de tickets) é empurrado para filas (Background Workers), evitando que a tela do usuário congele.