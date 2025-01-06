from app import db
from datetime import datetime

class Settings(db.Model):
    """Modelo para almacenar la configuración del sistema"""
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), unique=True, nullable=False)
    value = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @staticmethod
    def get_value(key, default=None):
        """Obtener el valor de una configuración"""
        setting = Settings.query.filter_by(key=key).first()
        return setting.value if setting else default

    @staticmethod
    def set_value(key, value):
        """Establecer el valor de una configuración"""
        setting = Settings.query.filter_by(key=key).first()
        if setting:
            setting.value = value
        else:
            setting = Settings(key=key, value=value)
            db.session.add(setting)
        db.session.commit()

    @staticmethod
    def get_all():
        """Obtener todas las configuraciones como diccionario"""
        settings = Settings.query.all()
        return {s.key: s.value for s in settings}

    def __repr__(self):
        return f'<Settings {self.key}={self.value}>' 