from app import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
        nome = db.Column(db.String(100), nullable=False)
            email = db.Column(db.String(120), unique=True, nullable=False)
                senha = db.Column(db.String(200), nullable=False)
                    # Define se é 'cliente', 'atendente' ou 'admin'
                        tipo = db.Column(db.String(20), nullable=False, default='cliente') 
                            
                                # Relação com os tickets e respostas
                                    tickets = db.relationship('Ticket', backref='cliente', lazy=True)
                                        respostas = db.relationship('Reply', backref='autor', lazy=True)

                                        class Ticket(db.Model):
                                            id = db.Column(db.Integer, primary_key=True)
                                                titulo = db.Column(db.String(150), nullable=False)
                                                    descricao = db.Column(db.Text, nullable=False)
                                                        status = db.Column(db.String(50), default='Aberto') 
                                                            data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
                                                                
                                                                    # NOVA COLUNA: Armazena a avaliação de 1 a 5 (começa vazia)
                                                                        nota = db.Column(db.Integer, nullable=True) 
                                                                            
                                                                                cliente_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
                                                                                    respostas = db.relationship('Reply', backref='ticket_original', lazy=True)

                                                                                    class Reply(db.Model):
                                                                                        id = db.Column(db.Integer, primary_key=True)
                                                                                            texto = db.Column(db.Text, nullable=False)
                                                                                                data_resposta = db.Column(db.DateTime, default=datetime.utcnow)
                                                                                                    
                                                                                                        # Chaves estrangeiras ligando ao ticket e ao autor (User)
                                                                                                            ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'), nullable=False)
                                                                                                                autor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)