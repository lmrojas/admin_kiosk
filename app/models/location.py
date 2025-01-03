from datetime import datetime
from app import db

class KioskLocation(db.Model):
    """Modelo para el histórico de ubicaciones de kiosks"""
    __tablename__ = 'kiosk_locations'
    
    id = db.Column(db.Integer, primary_key=True)
    kiosk_id = db.Column(db.Integer, db.ForeignKey('kiosks.id'), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime)
    notes = db.Column(db.String(255))
    
    # Relaciones
    kiosk = db.relationship('Kiosk', backref='location_history')
    location = db.relationship('Location')
    
    def __repr__(self):
        return f'<KioskLocation {self.kiosk.name} at {self.location.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'kiosk_id': self.kiosk_id,
            'location_id': self.location_id,
            'location': self.location.to_dict(),
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'notes': self.notes
        }

class Location(db.Model):
    __tablename__ = 'locations'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relaciones
    kiosks = db.relationship('Kiosk', backref='current_location', lazy=True)
    
    def __repr__(self):
        return f'<Location {self.name}>'
    
    def to_dict(self):
        """Convertir el objeto a un diccionario para la API"""
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_active': self.is_active
        }
    
    @staticmethod
    def get_active_locations():
        """Obtener todas las ubicaciones activas"""
        return Location.query.filter_by(is_active=True).all()
    
    @staticmethod
    def get_location_by_id(location_id):
        """Obtener una ubicación por su ID"""
        return Location.query.get_or_404(location_id)
    
    def update(self, data):
        """Actualizar los datos de la ubicación"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    def delete(self):
        """Eliminar la ubicación (soft delete)"""
        self.is_active = False
        self.updated_at = datetime.utcnow()
        db.session.commit() 