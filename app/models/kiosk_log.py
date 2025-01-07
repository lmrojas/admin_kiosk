from app.extensions import db
from datetime import datetime

class KioskLog(db.Model):
    """Modelo para el registro de eventos de los kiosks"""
    __tablename__ = 'kiosk_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    kiosk_id = db.Column(db.Integer, db.ForeignKey('kiosk.id'), nullable=False)
    event_type = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(500), nullable=False)
    details = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    created_by = db.Column(db.String(100))
    
    # Tipos de eventos predefinidos
    EVENT_TYPES = {
        'info': 'Información',
        'warning': 'Advertencia',
        'error': 'Error',
        'success': 'Éxito',
        'alert': 'Alerta',
        'action': 'Acción',
        'state': 'Estado',
        'location': 'Ubicación'
    }
    
    @property
    def event_type_display(self):
        """Obtiene el nombre para mostrar del tipo de evento"""
        return self.EVENT_TYPES.get(self.event_type, self.event_type)
    
    def to_dict(self):
        """Convierte el log a diccionario"""
        return {
            'id': self.id,
            'kiosk_id': self.kiosk_id,
            'event_type': self.event_type,
            'event_type_display': self.event_type_display,
            'message': self.message,
            'details': self.details,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'created_by': self.created_by
        }
    
    @classmethod
    def create_log(cls, kiosk_id, event_type, message, details=None, created_by=None):
        """Crea un nuevo registro de log"""
        log = cls(
            kiosk_id=kiosk_id,
            event_type=event_type,
            message=message,
            details=details,
            created_by=created_by
        )
        db.session.add(log)
        db.session.commit()
        return log
    
    def __repr__(self):
        return f'<KioskLog {self.event_type} for Kiosk {self.kiosk_id}>' 