from app.extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    """Modelo para los usuarios del sistema"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def set_password(self, password):
        """Establecer el hash de la contraseña"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verificar la contraseña"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convertir el objeto a un diccionario para la API"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_admin': self.is_admin,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @staticmethod
    def get_by_username(username):
        """Obtener un usuario por su nombre de usuario"""
        return User.query.filter_by(username=username).first()
    
    @staticmethod
    def get_by_email(email):
        """Obtener un usuario por su email"""
        return User.query.filter_by(email=email).first()
    
    @staticmethod
    def get_active_users():
        """Obtener todos los usuarios activos"""
        return User.query.filter_by(is_active=True).all() 