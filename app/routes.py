from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User, Ticket, Reply
from app import db

# Criação do Blueprint (um "pacote" de rotas)
bp = Blueprint('main', __name__)

# --- ROTAS DE AUTENTICAÇÃO ---

@bp.route('/registrar', methods=['GET', 'POST'])
def registrar():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')

        # Verifica se o email já existe
        if User.query.filter_by(email=email).first():
            flash('Este e-mail já está cadastrado no sistema.')
            return redirect(url_for('main.registrar'))

        senha_hash = generate_password_hash(senha)
        novo_usuario = User(nome=nome, email=email, senha=senha_hash, tipo='cliente')
        db.session.add(novo_usuario)
        db.session.commit()
        
        flash('Cadastro realizado com sucesso! Faça o seu login.')
        return redirect(url_for('main.login'))
        
    return render_template('registrar.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        user = User.query.filter_by(email=email).first()

        # Verifica usuário e se a senha está correta
        if user and check_password_hash(user.senha, senha):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        else:
            flash('E-mail ou senha incorretos.')
            
    return render_template('login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

# --- ROTAS PRINCIPAIS (HELP DESK) ---

@bp.route('/')
@login_required
def dashboard():
    # Clientes veem apenas os próprios chamados; Admin/Atendentes veem todos
    if current_user.tipo == 'cliente':
        tickets = Ticket.query.filter_by(cliente_id=current_user.id).all()
    else:
        tickets = Ticket.query.all()
        
    return render_template('dashboard.html', tickets=tickets)

@bp.route('/ticket/novo', methods=['GET', 'POST'])
@login_required
def novo_ticket():
    # Apenas clientes abrem chamados
    if current_user.tipo != 'cliente':
        flash('Apenas clientes podem abrir novas solicitações.')
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        titulo = request.form.get('titulo')
        descricao = request.form.get('descricao')
        
        ticket = Ticket(titulo=titulo, descricao=descricao, cliente_id=current_user.id)
        db.session.add(ticket)
        db.session.commit()
        
        flash('Chamado aberto com sucesso!')
        return redirect(url_for('main.dashboard'))
        
    return render_template('novo_ticket.html')

@bp.route('/ticket/<int:id>', methods=['GET', 'POST'])
@login_required
def ver_ticket(id):
    ticket = Ticket.query.get_or_404(id)

    if request.method == 'POST':
        texto_resposta = request.form.get('texto')
        resposta = Reply(texto=texto_resposta, ticket_id=ticket.id, autor_id=current_user.id)
        db.session.add(resposta)

        # Se um atendente responde, muda o status do chamado
        if current_user.tipo == 'atendente':
            ticket.status = 'Em Andamento'

        db.session.commit()
        return redirect(url_for('main.ver_ticket', id=ticket.id))

    return render_template('ticket.html', ticket=ticket)

# --- ROTAS DE ADMINISTRAÇÃO ---

@bp.route('/admin/atendentes/novo', methods=['GET', 'POST'])
@login_required
def novo_atendente():
    if current_user.tipo != 'admin':
        flash('Acesso negado. Apenas administradores podem cadastrar a equipe.')
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')

        if User.query.filter_by(email=email).first():
            flash('Este e-mail já está em uso.')
            return redirect(url_for('main.novo_atendente'))

        senha_hash = generate_password_hash(senha)
        atendente = User(nome=nome, email=email, senha=senha_hash, tipo='atendente')
        db.session.add(atendente)
        db.session.commit()
        
        flash('Novo atendente cadastrado com sucesso!')
        return redirect(url_for('main.dashboard'))
        
    return render_template('novo_atendente.html')

@bp.route('/admin/relatorios')
@login_required
def relatorios():
    if current_user.tipo != 'admin':
        flash('Acesso negado. Apenas administradores visualizam métricas.')
        return redirect(url_for('main.dashboard'))

    # Coleta de métricas do banco de dados
    abertos = Ticket.query.filter_by(status='Aberto').count()
    andamento = Ticket.query.filter_by(status='Em Andamento').count()
    resolvidos = Ticket.query.filter_by(status='Resolvido').count()

    return render_template('relatorios.html', abertos=abertos, andamento=andamento, resolvidos=resolvidos)