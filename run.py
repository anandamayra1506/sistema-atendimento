from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash
import os

app = create_app()

# Contexto da aplicação para mexer no banco de dados antes do servidor ligar
with app.app_context():
    # Cria o arquivo database.db na pasta instance automaticamente
    db.create_all()
    
    # Dados do admin inicial (busca do .env ou usa o padrão)
    admin_email = os.environ.get('ADMIN_EMAIL', 'admin@resolveai.com')
    admin_senha = os.environ.get('ADMIN_PASSWORD', 'senha_segura_123')
    
    # Verifica se o administrador já existe no banco
    admin_existente = User.query.filter_by(email=admin_email).first()
    
    if not admin_existente:
        # Criptografa a senha antes de salvar
        senha_hash = generate_password_hash(admin_senha)
        novo_admin = User(
            nome='Administrador Chefe', 
            email=admin_email, 
            senha=senha_hash, 
            tipo='admin'
        )
        db.session.add(novo_admin)
        db.session.commit()
        print("✅ Administrador inicial criado com sucesso no banco de dados!")
    else:
        print("✅ Banco de dados pronto. Administrador já existente.")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)