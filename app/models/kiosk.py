from app import db
from datetime import datetime
import json

class Kiosk(db.Model):
    """Modelo para los kiosks"""
    __tablename__ = 'kiosks'
    
    id = db.Column(db.Integer, primary_key=True)
    serial_number = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    location_text = db.Column(db.String(255))
    ip_address = db.Column(db.String(15))
    status = db.Column(db.String(50), default='offline')
    last_connection = db.Column(db.DateTime)
    last_action_state = db.Column(db.String(100))
    sensors_data = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
    state_id = db.Column(db.Integer, db.ForeignKey('states.id'))
    logs = db.relationship('KioskLog', backref='kiosk', lazy=True)
    
    # Umbrales de alerta
    THRESHOLDS = {
        'cpu': {'warning': 80, 'critical': 90},
        'ram': {'warning': 85, 'critical': 95},
        'disk': {'warning': 85, 'critical': 95},
        'temperature': {'warning': 35, 'critical': 40},
        'signal': {'warning': 30},
        'battery': {'critical': 10}
    }
    
    @property
    def sensors_data_dict(self):
        """Obtener los datos de sensores como diccionario"""
        if not self.sensors_data:
            return {}
        if isinstance(self.sensors_data, str):
            try:
                return json.loads(self.sensors_data)
            except json.JSONDecodeError:
                return {}
        return self.sensors_data if isinstance(self.sensors_data, dict) else {}
    
    def __repr__(self):
        return f'<Kiosk {self.name}>'
    
    def to_dict(self):
        """Convertir el objeto a un diccionario para la API"""
        return {
            'id': self.id,
            'serial_number': self.serial_number,
            'name': self.name,
            'location_text': self.location_text,
            'ip_address': self.ip_address,
            'status': self.status,
            'last_connection': self.last_connection.isoformat() if self.last_connection else None,
            'last_action_state': self.last_action_state,
            'sensors_data': self.sensors_data_dict,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'location': self.location.to_dict() if self.location else None,
            'state': self.state.to_dict() if self.state else None,
            'alerts': self.calculate_alerts()
        }
    
    def update_sensor_data(self, data):
        """Actualizar los datos de los sensores"""
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except json.JSONDecodeError:
                return False
        
        # Validar estructura de datos
        required_fields = ['cpu_usage', 'ram_usage', 'disk_usage']
        if not all(field in data for field in required_fields):
            return False
        
        # Actualizar datos y calcular alertas
        self.sensors_data = data
        self.updated_at = datetime.utcnow()
        
        # Actualizar estado basado en alertas
        alerts = self.calculate_alerts()
        if any(alert['type'] == 'danger' for alert in alerts):
            self.state_id = 3  # Estado crítico
        elif any(alert['type'] == 'warning' for alert in alerts):
            self.state_id = 2  # Estado warning
        else:
            self.state_id = 1  # Estado normal
        
        db.session.commit()
        return True
    
    def calculate_alerts(self):
        """Calcular alertas basadas en los datos de los sensores"""
        alerts = []
        data = self.sensors_data_dict
        if not data:
            return alerts
        
        # Sistema
        if 'cpu_usage' in data:
            cpu = float(data['cpu_usage'])
            if cpu > self.THRESHOLDS['cpu']['critical']:
                alerts.append({'type': 'danger', 'message': f'CPU crítico: {cpu}%'})
            elif cpu > self.THRESHOLDS['cpu']['warning']:
                alerts.append({'type': 'warning', 'message': f'CPU alto: {cpu}%'})
        
        if 'ram_usage' in data:
            ram = float(data['ram_usage'])
            if ram > self.THRESHOLDS['ram']['critical']:
                alerts.append({'type': 'danger', 'message': f'RAM crítico: {ram}%'})
            elif ram > self.THRESHOLDS['ram']['warning']:
                alerts.append({'type': 'warning', 'message': f'RAM alto: {ram}%'})
        
        if 'disk_usage' in data:
            disk = float(data['disk_usage'])
            if disk > self.THRESHOLDS['disk']['critical']:
                alerts.append({'type': 'danger', 'message': f'Disco crítico: {disk}%'})
            elif disk > self.THRESHOLDS['disk']['warning']:
                alerts.append({'type': 'warning', 'message': f'Disco alto: {disk}%'})
        
        # Ambiente
        if 'temperature' in data:
            temp = float(data['temperature'])
            if temp > self.THRESHOLDS['temperature']['critical']:
                alerts.append({'type': 'danger', 'message': f'Temperatura crítica: {temp}°C'})
            elif temp > self.THRESHOLDS['temperature']['warning']:
                alerts.append({'type': 'warning', 'message': f'Temperatura alta: {temp}°C'})
        
        # Red
        if 'network' in data:
            signal = float(data['network'].get('signal_strength', 100))
            if signal < self.THRESHOLDS['signal']['warning']:
                alerts.append({'type': 'warning', 'message': f'Señal WiFi baja: {signal}%'})
        
        # UPS
        if 'ups' in data:
            battery = float(data['ups'].get('battery_level', 100))
            if battery < self.THRESHOLDS['battery']['critical']:
                alerts.append({'type': 'danger', 'message': f'Batería crítica: {battery}%'})
        
        # Errores y advertencias explícitas
        alerts.extend({'type': 'danger', 'message': error} for error in data.get('errors', []))
        alerts.extend({'type': 'warning', 'message': warning} for warning in data.get('warnings', []))
        
        return alerts
    
    @staticmethod
    def get_kiosk_by_id(kiosk_id):
        """Obtener un kiosk por su ID"""
        return Kiosk.query.get_or_404(kiosk_id)
    
    @staticmethod
    def get_kiosk_by_serial(serial_number):
        """Obtener un kiosk por su número de serie"""
        return Kiosk.query.filter_by(serial_number=serial_number).first()
    
    @staticmethod
    def get_all_kiosks():
        """Obtener todos los kiosks"""
        return Kiosk.query.all() 