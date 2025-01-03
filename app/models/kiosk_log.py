from app import db
from datetime import datetime

class KioskLog(db.Model):
    """Modelo para los logs de los kiosks"""
    __tablename__ = 'kiosk_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    kiosk_id = db.Column(db.Integer, db.ForeignKey('kiosks.id'), nullable=False)
    event_type = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    details = db.Column(db.JSON)
    trace_id = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<KioskLog {self.event_type}: {self.message}>'
    
    def get_event_type_class(self):
        """Obtener la clase CSS para el tipo de evento"""
        type_classes = {
            'error': 'danger',
            'warning': 'warning',
            'info': 'info',
            'success': 'success',
            'system': 'primary',
            'action': 'secondary'
        }
        return type_classes.get(self.event_type.lower(), 'secondary')
    
    def to_dict(self):
        """Convertir el objeto a un diccionario para la API"""
        return {
            'id': self.id,
            'kiosk_id': self.kiosk_id,
            'event_type': self.event_type,
            'message': self.message,
            'details': self.details,
            'trace_id': self.trace_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    @staticmethod
    def log_event(kiosk_id, event_type, message, details=None, trace_id=None):
        """Registrar un evento en el log"""
        log = KioskLog(
            kiosk_id=kiosk_id,
            event_type=event_type,
            message=message,
            details=details,
            trace_id=trace_id
        )
        db.session.add(log)
        db.session.commit()
        return log 