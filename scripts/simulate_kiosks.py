"""Script para simular kioscos con diferentes comportamientos"""
import sys
import os
import random
import time
import socketio
import json
from datetime import datetime, timedelta, UTC
from threading import Thread, Event

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.extensions import db
from app.models import Kiosk, Location, KioskLog, State

# Configuración de comportamientos
BEHAVIORS = {
    'normal': {
        'probability': 0.6,  # 60% de los kiosks
        'cpu_range': (20, 60),
        'ram_range': (30, 70),
        'disk_range': (40, 75),
        'temp_range': (25, 32),
        'error_prob': 0.05,
        'warning_prob': 0.1,
        'offline_prob': 0.02,
        'location_mismatch_prob': 0.01
    },
    'stressed': {
        'probability': 0.3,  # 30% de los kiosks
        'cpu_range': (75, 95),
        'ram_range': (80, 95),
        'disk_range': (85, 95),
        'temp_range': (35, 42),
        'error_prob': 0.2,
        'warning_prob': 0.4,
        'offline_prob': 0.1,
        'location_mismatch_prob': 0.05
    },
    'problematic': {
        'probability': 0.1,  # 10% de los kiosks
        'cpu_range': (90, 100),
        'ram_range': (90, 100),
        'disk_range': (95, 100),
        'temp_range': (40, 48),
        'error_prob': 0.4,
        'warning_prob': 0.6,
        'offline_prob': 0.3,
        'location_mismatch_prob': 0.2
    }
}

class KioskSimulator:
    """Clase para simular el comportamiento de un kiosk"""
    
    def __init__(self, kiosk_id, behavior_type):
        self.kiosk_id = kiosk_id
        self.behavior = BEHAVIORS[behavior_type]
        self.sio = socketio.Client()
        self.connected = False
        self.stop_event = Event()
        self.last_location_check = datetime.now()
        
        # Configurar eventos de Socket.IO
        self.setup_socketio_events()
    
    def setup_socketio_events(self):
        """Configurar eventos de Socket.IO"""
        @self.sio.event
        def connect():
            print(f'Kiosk {self.kiosk_id} conectado')
            self.connected = True
            self.join_kiosk_room()
        
        @self.sio.event
        def disconnect():
            print(f'Kiosk {self.kiosk_id} desconectado')
            self.connected = False
        
        @self.sio.event
        def execute_action(data):
            print(f'Kiosk {self.kiosk_id} recibió acción: {data}')
            # Simular ejecución de acción
            time.sleep(random.uniform(0.5, 2.0))
            self.sio.emit('action_completed', {
                'kiosk_id': self.kiosk_id,
                'action_id': data['action_id'],
                'status': 'success'
            })
    
    def join_kiosk_room(self):
        """Unirse a la sala específica del kiosk"""
        self.sio.emit('join', {'kiosk_id': self.kiosk_id})
    
    def generate_sensor_data(self):
        """Generar datos simulados de sensores"""
        return {
            'cpu_usage': random.uniform(*self.behavior['cpu_range']),
            'ram_usage': random.uniform(*self.behavior['ram_range']),
            'disk_usage': random.uniform(*self.behavior['disk_range']),
            'temperature': random.uniform(*self.behavior['temp_range']),
            'network': {
                'latency': random.uniform(50, 200),
                'download_speed': random.uniform(1, 100),
                'upload_speed': random.uniform(1, 50),
                'signal_strength': random.uniform(-70, -30)
            },
            'ups': {
                'status': random.choice(['online', 'battery', 'bypass']),
                'battery_level': random.uniform(20, 100),
                'estimated_runtime': random.randint(10, 120)
            }
        }
    
    def check_location_mismatch(self, app):
        """Verificar y actualizar discrepancia de ubicación"""
        if (datetime.now() - self.last_location_check).seconds > 300:  # Cada 5 minutos
            with app.app_context():
                kiosk = Kiosk.query.get(self.kiosk_id)
                if kiosk and random.random() < self.behavior['location_mismatch_prob']:
                    # Simular movimiento del kiosk
                    kiosk.current_latitude = kiosk.location.latitude + random.uniform(-0.01, 0.01)
                    kiosk.current_longitude = kiosk.location.longitude + random.uniform(-0.01, 0.01)
                    kiosk.location_mismatch = True
                    
                    # Registrar el evento
                    KioskLog.create_log(
                        kiosk_id=kiosk.id,
                        event_type='location',
                        message='Discrepancia de ubicación detectada',
                        details={
                            'current_location': {
                                'lat': kiosk.current_latitude,
                                'lng': kiosk.current_longitude
                            },
                            'assigned_location': {
                                'lat': kiosk.location.latitude,
                                'lng': kiosk.location.longitude
                            }
                        }
                    )
                    db.session.commit()
            self.last_location_check = datetime.now()
    
    def run(self, app):
        """Ejecutar el simulador"""
        while not self.stop_event.is_set():
            try:
                if not self.connected:
                    try:
                        self.sio.connect('http://localhost:5000')
                    except Exception as e:
                        print(f'Error conectando kiosk {self.kiosk_id}: {str(e)}')
                        time.sleep(5)
                        continue
                
                # Simular comportamiento offline
                if random.random() < self.behavior['offline_prob']:
                    if self.connected:
                        self.sio.disconnect()
                    time.sleep(random.uniform(5, 15))
                    continue
                
                # Generar y enviar datos
                with app.app_context():
                    kiosk = Kiosk.query.get(self.kiosk_id)
                    if kiosk:
                        # Actualizar estado y datos
                        sensors_data = self.generate_sensor_data()
                        kiosk.last_connection = datetime.now(UTC)
                        kiosk.sensors_data = sensors_data
                        
                        # Verificar ubicación
                        self.check_location_mismatch(app)
                        
                        # Enviar actualización por WebSocket
                        if self.connected:
                            self.sio.emit('kiosk_update', {
                                'kiosk_id': self.kiosk_id,
                                'data': {
                                    'status': 'online',
                                    'sensors_data': sensors_data,
                                    'last_connection': kiosk.last_connection.isoformat()
                                }
                            })
                        
                        db.session.commit()
                
                # Esperar antes de la siguiente actualización
                time.sleep(random.uniform(1, 3))
                
            except Exception as e:
                print(f'Error en kiosk {self.kiosk_id}: {str(e)}')
                time.sleep(5)
    
    def stop(self):
        """Detener el simulador"""
        self.stop_event.set()
        if self.connected:
            self.sio.disconnect()

def create_test_kiosks(num_kiosks=10):
    """Crear kiosks de prueba"""
    app = create_app()
    with app.app_context():
        locations = Location.query.all()
        normal_state = State.query.filter_by(name='Normal').first()
        
        for i in range(num_kiosks):
            # Asignar comportamiento basado en probabilidades
            rand = random.random()
            if rand < BEHAVIORS['normal']['probability']:
                behavior = 'normal'
            elif rand < BEHAVIORS['normal']['probability'] + BEHAVIORS['stressed']['probability']:
                behavior = 'stressed'
            else:
                behavior = 'problematic'
            
            # Crear kiosk
            location = random.choice(locations)
            kiosk = Kiosk(
                name=f'Kiosk Test {i+1:03d}',
                serial_number=f'SN{random.randint(10000000, 99999999)}',
                status='offline',
                location=location,
                current_latitude=location.latitude,
                current_longitude=location.longitude,
                state=normal_state,
                ip_address=f'192.168.1.{random.randint(2, 254)}'
            )
            db.session.add(kiosk)
        
        db.session.commit()
        return [(k.id, 'normal' if random.random() < 0.6 else 'stressed' if random.random() < 0.8 else 'problematic') 
                for k in Kiosk.query.all()]

def main():
    """Función principal"""
    # Crear kiosks de prueba
    kiosk_configs = create_test_kiosks(10)
    
    # Crear y ejecutar simuladores
    simulators = []
    app = create_app()
    
    try:
        # Iniciar simuladores
        for kiosk_id, behavior in kiosk_configs:
            simulator = KioskSimulator(kiosk_id, behavior)
            thread = Thread(target=simulator.run, args=(app,))
            thread.daemon = True
            thread.start()
            simulators.append((simulator, thread))
            print(f'Iniciado simulador para Kiosk {kiosk_id} con comportamiento {behavior}')
        
        # Mantener el script corriendo
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nDeteniendo simuladores...")
        for simulator, _ in simulators:
            simulator.stop()
        
        print("Simulación finalizada")

if __name__ == '__main__':
    main() 