from app.extensions import db
from datetime import datetime

class Location(db.Model):
    """Modelo para las ubicaciones"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    kiosks = db.relationship('Kiosk', back_populates='location', lazy='joined')
    kiosk_history = db.relationship('KioskLocation', back_populates='location',
                                  cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convierte la ubicación a diccionario"""
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'description': self.description or '',
            'kiosks_count': len(self.kiosks),
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def __repr__(self):
        return f'<Location {self.name}>' 