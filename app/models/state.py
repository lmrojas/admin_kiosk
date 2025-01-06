from app.extensions import db
from datetime import datetime

class State(db.Model):
    """Modelo para los estados de los kiosks"""
    __tablename__ = 'states'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(200))
    color_class = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relaciones
    kiosks = db.relationship('Kiosk', back_populates='state', lazy='dynamic')
    
    def __repr__(self):
        return f'<State {self.name}>'
    
    def to_dict(self):
        """Convierte el estado a un diccionario"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'color_class': self.color_class,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_active': self.is_active
        } 