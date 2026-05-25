# Relatório de Inspeção de Segurança - ResolveAí

**Nível de Profundidade:** PROFUNDA
**Alvo:** Código-fonte principal (`app/routes.py`, `app/models.py`, `templates/`, `run.py`)

---

## 1. Resumo Executivo
A inspeção profunda de cibersegurança no sistema Help Desk identificou vulnerabilidades que necessitam de mitigação para garantir a integridade dos dados e a segurança dos usuários. 

**Contagem de Achados por Severidade:**
* **Crítica:** 1
* **Alta:** 2
* **Média:** 2
* **Baixa:** 0

### As 5 Ações Mais Urgentes:
1. **Corrigir falha de IDOR:** Impedir que um cliente acesse tickets de terceiros manipulando a URL.
2. **Desativar o Modo Debug:** Remover a flag de debug do ambiente de produção para evitar vazamento de variáveis de ambiente.
3. **Implementar Proteção CSRF:** Adicionar tokens de validação nos formulários de login e avaliação.
4. **Reforçar Política de Senhas:** Exigir complexidade mínima no cadastro de novos usuários.
5. **Implementar Trilha de Auditoria (Logs):** Registrar eventos críticos (falhas de login e alteração de status de chamados).

---

## 2. Detalhamento das Vulnerabilidades

### Vulnerabilidade 1: Insecure Direct Object Reference (IDOR)
* **Localização:** `app/routes.py` (Rota `/ticket/<id>`)
* **Descrição:** O sistema busca o ticket pelo ID informado na URL, mas não verifica se o usuário logado (quando perfil 'cliente') é o verdadeiro dono daquele ticket.
* **Evidência:** `ticket = Ticket.query.get_or_404(id)` seguido diretamente pela renderização do template, sem checar a posse.
* **Impacto:** Um cliente mal-intencionado pode alterar o número na URL e ler chamados confidenciais de outras pessoas.
* **Severidade:** **Crítica**
* **Recomendação:** Adicionar validação de posse garantindo que o `cliente_id` do ticket seja idêntico ao `id` do usuário logado.
* **Referências:** OWASP A01:2021-Broken Access Control | CWE-284

### Vulnerabilidade 2: Exposição de Informações Sensíveis via Debug
* **Localização:** `docker-compose.yml` e `run.py`
* **Descrição:** A variável de ambiente do Flask está configurada para expor o console de debug interativo em caso de falhas.
* **Evidência:** `FLASK_DEBUG=1` e `app.run(debug=True)`.
* **Impacto:** Se o sistema estourar um erro, o invasor terá acesso ao console interativo do Werkzeug, podendo ler chaves e executar comandos.
* **Severidade:** **Alta**
* **Recomendação:** Alterar para `FLASK_DEBUG=0` em produção e remover a tag de debug do arquivo de inicialização.
* **Referências:** OWASP A05:2021-Security Misconfiguration | CWE-209

### Vulnerabilidade 3: Ausência de Proteção Cross-Site Request Forgery (CSRF)
* **Localização:** `templates/ticket.html` (Formulário de Avaliação e Resposta)
* **Descrição:** Os formulários que alteram o estado do sistema (POST) não possuem um Token CSRF para validar a origem da requisição.
* **Evidência:** Formulários sem o campo de input invisível com o `csrf_token`.
* **Impacto:** Um atacante pode enganar um Atendente logado fazendo-o clicar em um link malicioso que envia uma requisição forjada.
* **Severidade:** **Alta**
* **Recomendação:** Integrar a biblioteca `Flask-WTF` e utilizar a função `CSRFProtect(app)`.
* **Referências:** OWASP A01:2021-Broken Access Control | CWE-352


### Vulnerabilidade 4: Falhas de Autenticação (Política de Senhas Fraca)
* **Localização:** `app/routes.py` (Rota `/registrar`)
* **Descrição:** O sistema aplica o hash na senha, o que é correto, mas não exige complexidade ou tamanho mínimo antes da conversão.
* **Evidência:** Validação restrita apenas a checar se o campo não está vazio antes de salvar.
* **Impacto:** Usuários podem cadastrar senhas como "123456", tornando o sistema vulnerável a ataques de força bruta.
* **Severidade:** **Média**
* **Recomendação:** Adicionar Expressão Regular (Regex) para exigir no mínimo 8 caracteres, letras, números e caracteres especiais.
* **Referências:** OWASP A07:2021-Identification and Authentication Failures | CWE-521

### Vulnerabilidade 5: Falta de Monitoramento e Logs de Segurança
* **Localização:** Aplicação Global (`app/__init__.py`)
* **Descrição:** A aplicação não registra falhas de login, bloqueios de acesso ou erros de sistema em um arquivo de log auditável.
* **Evidência:** Ausência de importação da biblioteca `logging` do Python.
* **Impacto:** Em caso de invasão, os administradores não terão rastreabilidade forense para descobrir a origem do ataque.
* **Severidade:** **Média**
* **Recomendação:** Configurar o módulo de log nativo do Python gravando arquivos em modo `RotatingFileHandler`.
* **Referências:** OWASP A09:2021-Security Logging and Alerting Failures | CWE-778
