from app.extensions import db
from datetime import datetime

class Location(db.Model):
    """Modelo para las ubicaciones"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    kiosks = db.relationship('Kiosk', back_populates='location')
    
    @classmethod
    def get_active_locations(cls):
        """Obtiene todas las ubicaciones activas"""
        return cls.query.filter_by(is_active=True).all()
    
    def to_dict(self):
        """Convierte la ubicación a diccionario"""
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'is_active': self.is_active,
            'kiosks_count': len(self.kiosks),
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def __repr__(self):
        return f'<Location {self.name}>'

class KioskLocation(db.Model):
    """Modelo para el historial de ubicaciones de kiosks"""
    id = db.Column(db.Integer, primary_key=True)
    kiosk_id = db.Column(db.Integer, db.ForeignKey('kiosk.id'), index=True)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), index=True)
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime)
    notes = db.Column(db.String(200))
    
    def to_dict(self):
        """Convierte el registro a diccionario"""
        return {
            'id': self.id,
            'kiosk_id': self.kiosk_id,
            'location_id': self.location_id,
            'start_date': self.start_date.strftime('%Y-%m-%d %H:%M:%S'),
            'end_date': self.end_date.strftime('%Y-%m-%d %H:%M:%S') if self.end_date else None,
            'notes': self.notes
        }
    
    def __repr__(self):
        return f'<KioskLocation {self.kiosk_id} -> {self.location_id}>' 