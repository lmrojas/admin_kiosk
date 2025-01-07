"""Modelo para los kiosks"""
from app.extensions import db
from datetime import datetime
from sqlalchemy.dialects.sqlite import JSON
from app.services.alert_service import AlertService
from app.services.location_service import LocationService

class Kiosk(db.Model):
    """Modelo para los kiosks"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    serial_number = db.Column(db.String(50), unique=True, nullable=False)
    status = db.Column(db.String(20), default='offline')
    ip_address = db.Column(db.String(45))
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    current_latitude = db.Column(db.Float)
    current_longitude = db.Column(db.Float)
    location_mismatch = db.Column(db.Boolean, default=False)
    state_id = db.Column(db.Integer, db.ForeignKey('states.id'))
    last_connection = db.Column(db.DateTime)
    last_action_state = db.Column(db.String(100))
    sensors_data = db.Column(JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    location = db.relationship('Location', back_populates='kiosks')
    state = db.relationship('State', back_populates='kiosks')
    logs = db.relationship('KioskLog', backref='kiosk', lazy='dynamic',
                          cascade='all, delete-orphan')
    location_history = db.relationship('KioskLocation', back_populates='kiosk',
                                     cascade='all, delete-orphan')
    
    def check_location_mismatch(self):
        """Verifica si hay discrepancia entre la ubicación asignada y la real"""
        if not self.location:
            return False
            
        self.location_mismatch = LocationService.check_location_mismatch(
            self.current_latitude,
            self.current_longitude,
            self.location.latitude,
            self.location.longitude
        )
        return self.location_mismatch
    
    def calculate_alerts(self):
        """Calcula las alertas basadas en los sensores"""
        return AlertService.calculate_alerts(self.sensors_data)
    
    def change_location(self, new_location, notes=None):
        """Cambia la ubicación del kiosk y registra el cambio"""
        return LocationService.register_location_change(self, new_location, notes)
    
    def get_location_history(self, limit=10):
        """Obtiene el historial de ubicaciones"""
        return LocationService.get_location_history(self.id, limit)
    
    @property
    def sensors_data_dict(self):
        """Obtiene los datos de sensores como diccionario"""
        return self.sensors_data if self.sensors_data else {}
    
    def to_dict(self):
        """Convierte el kiosk a diccionario"""
        return {
            'id': self.id,
            'name': self.name,
            'serial_number': self.serial_number,
            'status': self.status,
            'ip_address': self.ip_address,
            'location_id': self.location_id,
            'location_name': self.location.name if self.location else None,
            'current_latitude': self.current_latitude,
            'current_longitude': self.current_longitude,
            'location_mismatch': self.location_mismatch,
            'last_connection': self.last_connection.strftime('%Y-%m-%d %H:%M:%S') if self.last_connection else None,
            'last_action_state': self.last_action_state,
            'sensors_data': self.sensors_data_dict,
            'alerts': self.calculate_alerts()
        }
    
    def __repr__(self):
        return f'<Kiosk {self.name}>' 