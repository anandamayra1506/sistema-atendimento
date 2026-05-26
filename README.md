# 🛠️ ResolveAí - Sistema de Help Desk

Um sistema completo de atendimento e gerenciamento de solicitações de suporte (Help Desk), desenvolvido com arquitetura MVT utilizando Python e Flask, rodando nativamente em contêineres Docker e otimizado para ambientes em nuvem.

### 🎓 Contexto Acadêmico
Este projeto foi desenvolvido como requisito avaliativo para a disciplina de **Desenvolvimento Web** (Abril e Maio/2026), ministrada pelo **Prof. Dr. Fábio Silveira Vidal**, no curso de **Pós-graduação Lato Sensu em Desenvolvimento de Sistemas Computacionais** do **Instituto Federal do Tocantins — Campus Araguatins**.

---

## 🎯 Visão Geral do Projeto

O **ResolveAí** centraliza a comunicação entre clientes e a equipe de suporte. O sistema possui controle hierárquico de acesso (RBAC), permitindo que os clientes abram chamados e os avaliem após a resolução, enquanto a equipe técnica interage para solucionar os problemas. Administradores possuem uma visão macro da operação através de relatórios em tempo real.

### Principais Funcionalidades e Melhorias
* **Gestão de Perfis (RBAC):** Três níveis de acesso estritos (Administrador, Atendente e Cliente).
* **Fluxo de Chamados (Tickets):** Abertura, interação via thread de mensagens e alteração automatizada de status (Aberto ➔ Em Andamento ➔ Resolvido).
* **Painel Gerencial Otimizado:** Relatórios em tempo real com implementação de **Cache** (`Flask-Caching`) para garantir alto desempenho do banco de dados em horários de pico.
* **Interface Responsiva e Acessível:** Frontend construído com Bootstrap 5, preparado para dispositivos móveis (Mobile-First), com tratamento visual de estados vazios (*Empty States*) e atributos de acessibilidade (ARIA labels).
* **Segurança Reforçada:** Sistema blindado com proteção contra Insecure Direct Object Reference (IDOR), falsificação de requisições (CSRF), e hash seguro de senhas.

---

## 💻 Tecnologias Utilizadas

* **Backend:** Python 3.10 | Flask (Micro-framework) | Flask-Caching | Flask-WTF
* **Frontend:** HTML5 | CSS3 | Bootstrap 5 | Jinja2 (Motor de Templates)
* **Banco de Dados:** SQLite (com ORM Flask-SQLAlchemy)
* **Infraestrutura:** Docker | Docker Compose | GitHub Codespaces
* **Controle de Versão:** Git | GitHub

---

## ⚙️ Como Executar o Projeto

Este projeto está configurado para rodar através do Docker. Você pode executá-lo diretamente na nuvem usando o GitHub Codespaces (recomendado) ou localmente na sua máquina.

### Alternativa 1: Rodando na Nuvem via GitHub Codespaces (Recomendado)
Esta é a maneira mais rápida de testar o sistema, pois não exige nenhuma instalação na sua máquina e resolve problemas de incompatibilidade de virtualização local (WSL).

1. Acesse este repositório no GitHub.
2. Clique no botão verde **`<> Code`**.
3. Mude para a aba **Codespaces** e clique em **Create codespace on main**.
4. Aguarde o ambiente do VS Code carregar no seu navegador.
5. No terminal integrado na parte inferior da tela, digite o comando para construir e rodar o contêiner:

        docker-compose up --build

6. O Codespaces exibirá uma notificação no canto inferior direito avisando que a aplicação está rodando na porta 5000. Clique em **Open in Browser** (Abrir no navegador) para acessar o sistema.

### Alternativa 2: Rodando Localmente
Caso prefira rodar no seu próprio computador, certifique-se de ter o Docker instalado.

1. **Clone o repositório:**

        git clone https://github.com/anandamayra1506/sistema-atendimento.git
        cd sistema-atendimento

2. **Construa e inicie o contêiner:**

        docker-compose up --build

3. **Acesse a aplicação:**
   Abra o seu navegador e acesse: `http://localhost:5000`

   ---

## 🔐 Perfis de Teste

Para testar o sistema logo após a inicialização, o banco de dados criará automaticamente um administrador padrão. Você também pode criar contas de cliente diretamente na tela inicial da aplicação.

**Administrador Inicial:**
* **E-mail:** `admin@resolveai.com`
* **Senha:** `senha_segura_123`

*(Nota: As credenciais acima são geradas a partir das variáveis de ambiente localizadas no arquivo docker-compose.yml).*

---

## 📂 Estrutura Principal de Diretórios

A arquitetura do projeto foi estruturada para manter a separação clara entre as regras de negócio, a interface e as especificações de engenharia de software exigidas pela disciplina.

    /
    ├── app/
    │   ├── templates/          # Interfaces responsivas (HTML + Jinja2 + Bootstrap)
    │   ├── __init__.py         # Configuração do Flask, Cache e Extensões
    │   ├── models.py           # Modelagem do Banco de Dados (SQLite)
    │   └── routes.py           # Controladores e Regras de Negócio (RBAC)
    ├── doc/
    │   ├── 03-especs.md        # Especificações do sistema, arquitetura e fluxo
    │   └── testing.md          # Plano de testes e validação de cenários críticos
    ├── instance/               # Armazena o database.db gerado em tempo de execução
    ├── Dockerfile              # Imagem do contêiner Python
    ├── docker-compose.yml      # Orquestração do serviço
    ├── refactor.md             # Relatório de otimização de desempenho e filas
    ├── relatorio_seguranca.md  # Auditoria de cibersegurança (Padrão OWASP Top 10)
    ├── requirements.txt        # Dependências do projeto
    └── run.py                  # Ponto de entrada (Entrypoint)

---

## 👩‍💻 Autoria

Desenvolvido por **Ananda Máyra Afonso Ferreira & IA**.