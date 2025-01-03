import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models.user import User
from werkzeug.security import generate_password_hash

def create_admin():
    """Crear usuario admin por defecto"""
    app = create_app()
    with app.app_context():
        # Verificar si ya existe el usuario admin
        admin = User.query.filter_by(username='admin').first()
        if admin:
            print('El usuario admin ya existe')
            return
        
        # Crear nuevo usuario admin
        admin = User(
            username='admin',
            password_hash=generate_password_hash('admin123'),
            email='admin@example.com',
            is_admin=True,
            is_active=True
        )
        
        try:
            db.session.add(admin)
            db.session.commit()
            print('Usuario admin creado exitosamente')
        except Exception as e:
            db.session.rollback()
            print(f'Error al crear usuario admin: {str(e)}')

if __name__ == '__main__':
    create_admin() 