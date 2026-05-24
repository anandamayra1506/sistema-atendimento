from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = 'chave_super_secreta_para_sessoes'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    # Configura o gerenciador de login
    login_manager.init_app(app)
    login_manager.login_view = 'main.login' # Redireciona não-logados pra cá
    login_manager.login_message = "Por favor, faça login para acessar esta página."
    
    # Ensina ao Flask como buscar o usuário logado no banco de dados
    from app.models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Registra o pacote de rotas (Blueprint) que criamos no routes.py
    from app.routes import bp
    app.register_blueprint(bp)
    
    return app