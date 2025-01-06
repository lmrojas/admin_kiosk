from app.extensions import db
from datetime import datetime

class KioskLog(db.Model):
    """Modelo para el registro de eventos de los kiosks"""
    __tablename__ = 'kiosk_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    kiosk_id = db.Column(db.Integer, db.ForeignKey('kiosk.id'))
    event_type = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Tipos de eventos predefinidos
    EVENT_TYPES = {
        'info': 'Información',
        'warning': 'Advertencia',
        'error': 'Error',
        'success': 'Éxito'
    }
    
    @property
    def event_type_display(self):
        """Obtiene el nombre para mostrar del tipo de evento"""
        return self.EVENT_TYPES.get(self.event_type, self.event_type)
    
    def __repr__(self):
        return f'<KioskLog {self.event_type}>' 