from app.extensions import db
from datetime import datetime

class KioskLocation(db.Model):
    """Modelo para registrar el historial de ubicaciones de los kioscos"""
    __tablename__ = 'kiosk_location'
    
    id = db.Column(db.Integer, primary_key=True)
    kiosk_id = db.Column(db.Integer, db.ForeignKey('kiosk.id'), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_date = db.Column(db.DateTime)
    
    # Relaciones
    kiosk = db.relationship('Kiosk', back_populates='location_history')
    location = db.relationship('Location', back_populates='kiosk_history')
    
    def __repr__(self):
        return f'<KioskLocation {self.kiosk_id} at {self.location_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'kiosk_id': self.kiosk_id,
            'location_id': self.location_id,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None
        } 