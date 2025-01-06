from app.extensions import db
from datetime import datetime

class Action(db.Model):
    """Modelo para las acciones que se pueden ejecutar en los kiosks"""
    __tablename__ = 'actions'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    command = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(200))
    icon_class = db.Column(db.String(50))
    requires_confirmation = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<Action {self.name}>'
    
    def to_dict(self):
        """Convierte la acción a un diccionario"""
        return {
            'id': self.id,
            'name': self.name,
            'command': self.command,
            'description': self.description,
            'icon_class': self.icon_class,
            'requires_confirmation': self.requires_confirmation,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_active': self.is_active
        } 