from app.extensions import db
from datetime import datetime
from sqlalchemy.dialects.sqlite import JSON

class Kiosk(db.Model):
    """Modelo para los kiosks"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    serial_number = db.Column(db.String(50), unique=True, nullable=False)
    status = db.Column(db.String(20), default='offline')
    ip_address = db.Column(db.String(45))
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
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
    
    @property
    def sensors_data_dict(self):
        """Obtiene los datos de sensores como diccionario"""
        return self.sensors_data if self.sensors_data else {}
    
    @property
    def alert_level(self):
        """Calcula el nivel de alerta basado en los sensores"""
        from app.models.settings import Settings
        
        if not self.sensors_data:
            return None
            
        cpu_warning = int(Settings.get_value('cpu_warning', 80))
        cpu_critical = int(Settings.get_value('cpu_critical', 90))
        ram_warning = int(Settings.get_value('ram_warning', 85))
        ram_critical = int(Settings.get_value('ram_critical', 95))
        
        cpu = float(self.sensors_data.get('cpu_usage', 0))
        ram = float(self.sensors_data.get('ram_usage', 0))
        
        if cpu >= cpu_critical or ram >= ram_critical:
            return 'critical'
        elif cpu >= cpu_warning or ram >= ram_warning:
            return 'warning'
        return 'normal'
    
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
            'last_connection': self.last_connection.strftime('%Y-%m-%d %H:%M:%S') if self.last_connection else None,
            'last_action_state': self.last_action_state,
            'sensors_data': self.sensors_data_dict,
            'alert_level': self.alert_level
        }
    
    def __repr__(self):
        return f'<Kiosk {self.name}>' 
    
    def calculate_alerts(self):
        """Calcula las alertas basadas en los sensores"""
        alerts = []
        
        if not self.sensors_data:
            return alerts
            
        # CPU
        cpu = float(self.sensors_data.get('cpu_usage', 0))
        if cpu > 90:
            alerts.append({
                'type': 'danger',
                'message': f'CPU crítico: {cpu:.1f}%'
            })
        elif cpu > 80:
            alerts.append({
                'type': 'warning',
                'message': f'CPU alto: {cpu:.1f}%'
            })
        
        # RAM
        ram = float(self.sensors_data.get('ram_usage', 0))
        if ram > 95:
            alerts.append({
                'type': 'danger',
                'message': f'RAM crítica: {ram:.1f}%'
            })
        elif ram > 85:
            alerts.append({
                'type': 'warning',
                'message': f'RAM alta: {ram:.1f}%'
            })
        
        # Disco
        disk = float(self.sensors_data.get('disk_usage', 0))
        if disk > 95:
            alerts.append({
                'type': 'danger',
                'message': f'Disco crítico: {disk:.1f}%'
            })
        elif disk > 85:
            alerts.append({
                'type': 'warning',
                'message': f'Disco alto: {disk:.1f}%'
            })
        
        # Temperatura
        temp = float(self.sensors_data.get('temperature', 0))
        if temp > 40:
            alerts.append({
                'type': 'danger',
                'message': f'Temperatura crítica: {temp:.1f}°C'
            })
        elif temp > 35:
            alerts.append({
                'type': 'warning',
                'message': f'Temperatura alta: {temp:.1f}°C'
            })
        
        # Red
        network = self.sensors_data.get('network', {})
        latency = float(network.get('latency', 0))
        if latency > 150:
            alerts.append({
                'type': 'danger',
                'message': f'Latencia crítica: {latency:.0f}ms'
            })
        elif latency > 100:
            alerts.append({
                'type': 'warning',
                'message': f'Latencia alta: {latency:.0f}ms'
            })
        
        # UPS
        ups = self.sensors_data.get('ups', {})
        if ups.get('status') == 'battery':
            battery = float(ups.get('battery_level', 0))
            runtime = int(ups.get('estimated_runtime', 0))
            if battery < 20:
                alerts.append({
                    'type': 'danger',
                    'message': f'Batería crítica: {battery:.1f}% ({runtime}min restantes)'
                })
            elif battery < 50:
                alerts.append({
                    'type': 'warning',
                    'message': f'En batería: {battery:.1f}% ({runtime}min restantes)'
                })
        
        return alerts 