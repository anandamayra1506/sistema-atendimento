# Relatório de Refatoração e Otimização
**Sistema:** ResolveAí (Help Desk)

## 1. Escopo das Alterações
Em conformidade com a Aula 09, o sistema passou por um processo de refatoração focado em três pilares: simplificação de código, ganho de desempenho computacional (Cache) e processamento em segundo plano (Jobs/Filas).

## 2. Simplificação e Modularização de Código (Clean Code)
A base de código foi revisada para eliminar redundâncias e acoplamentos desnecessários:
* **Isolamento de Lógica:** As verificações repetitivas de Controle de Acesso (RBAC) que poluíam o arquivo `routes.py` foram extraídas para *decorators* customizados (`@requer_admin`, `@requer_atendente`), tornando as rotas mais limpas e legíveis.
* **Redução de Duplicidade:** Consultas (Queries) repetidas no banco de dados com o SQLAlchemy foram unificadas em métodos auxiliares dentro do `models.py`.

## 3. Otimização de Desempenho (Cache)
Para evitar a sobrecarga do banco de dados relacional (SQLite), foi introduzida a camada de Cache na aplicação.
* **Implementação:** Utilização da extensão `Flask-Caching` com o backend `SimpleCache`.
* **Alvo de Otimização:** A rota do Dashboard do Proprietário (`/admin/dashboard`), que processa relatórios de volume de chamados. Como esses relatórios exigem consultas pesadas (Count/GroupBy) e não requerem tempo real absoluto, foi aplicado um tempo de vida útil (TTL) de 60 segundos no cache.
* **Benefício:** Redução drástica do uso de CPU e leitura de disco em momentos de pico de acessos.

## 4. Implementação de Jobs e Filas (Processamento Assíncrono)
Processos lentos que não dependem da interface visual foram removidos do ciclo de requisição principal HTTP.
* **Implementação:** Padrão de filas assíncronas (Background Workers) para ações demoradas.
* **Cenário Refatorado:** O disparo de "Notificações/Emails" gerado quando um chamado muda para o status "Resolvido". 
* **Benefício:** Em vez de fazer o cliente esperar o servidor enviar o e-mail para a sua caixa de entrada, o envio é empurrado para uma fila de processamento em segundo plano. A resposta web é devolvida imediatamente ao usuário, melhorando a Percepção de Performance (UX).

## 5. Atualização da Documentação e Dependências
Para refletir a nova arquitetura refatorada, os seguintes artefatos foram atualizados:
* **`requirements.txt`:** Inclusão das bibliotecas de otimização (`Flask-Caching==2.1.0`).
* **`doc/03-especs.md`:** A seção de Arquitetura Técnica foi atualizada para descrever as camadas de Cache e de Filas de Processamento de Notificações.
* **`doc/testing.md`:** Foram adicionados novos cenários para garantir que o Cache expire corretamente e que as tarefas em background não quebrem a integridade do banco de dados.

*O projeto mantém sua consistência arquitetural, sem ferir as especificações iniciais, sendo mais resiliente e escalável.*