from app.extensions import db

class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), unique=True, nullable=False)
    value = db.Column(db.String(200))
    description = db.Column(db.String(200))
    
    DEFAULT_SETTINGS = {
        'system_name': ('Admin Kiosk', 'Nombre del sistema'),
        'refresh_interval': ('5', 'Intervalo de actualización en segundos'),
        'max_logs': ('100', 'Máximo número de logs a mostrar'),
        'cpu_warning': ('80', 'Umbral de advertencia de CPU (%)'),
        'cpu_critical': ('90', 'Umbral crítico de CPU (%)'),
        'ram_warning': ('85', 'Umbral de advertencia de RAM (%)'),
        'ram_critical': ('95', 'Umbral crítico de RAM (%)'),
        'disk_warning': ('85', 'Umbral de advertencia de disco (%)'),
        'disk_critical': ('95', 'Umbral crítico de disco (%)'),
    }
    
    @classmethod
    def initialize_defaults(cls):
        """Inicializa las configuraciones por defecto si no existen"""
        for key, (value, description) in cls.DEFAULT_SETTINGS.items():
            if not cls.query.filter_by(key=key).first():
                setting = cls(key=key, value=value, description=description)
                db.session.add(setting)
        db.session.commit()
    
    @classmethod
    def get_value(cls, key, default=None):
        """Obtiene el valor de una configuración"""
        setting = cls.query.filter_by(key=key).first()
        return setting.value if setting else default
    
    @classmethod
    def set_value(cls, key, value):
        """Establece el valor de una configuración"""
        setting = cls.query.filter_by(key=key).first()
        if setting:
            setting.value = str(value)
            db.session.commit()
        else:
            description = cls.DEFAULT_SETTINGS.get(key, ('', ''))[1]
            setting = cls(key=key, value=str(value), description=description)
            db.session.add(setting)
            db.session.commit()
        return setting 