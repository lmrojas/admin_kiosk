import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import socketio
import time
import random
import json
from datetime import datetime
from app import create_app, db
from app.models.kiosk import Kiosk
from app.models.kiosk_log import KioskLog

# Crear cliente SocketIO
sio = socketio.Client()

# Configuración del kiosk simulado
KIOSK_DATA = {
    'id': 1,  # ID del kiosk a simular
    'serial_number': 'SIM001',
    'name': 'Kiosk Simulado',
    'status': 'online',
    'sensors_data': {
        'temperature': 25.0,
        'humidity': 50.0,
        'voltage': 120.0,
        'cpu_usage': 30.0,
        'memory_usage': 45.0
    }
}

@sio.event
def connect():
    print('Conectado al servidor WebSocket')
    # Enviar estado inicial
    send_kiosk_data()

@sio.event
def disconnect():
    print('Desconectado del servidor WebSocket')

def generate_sensor_data():
    """Generar datos aleatorios para los sensores"""
    return {
        'temperature': round(random.uniform(20.0, 30.0), 1),
        'humidity': round(random.uniform(40.0, 60.0), 1),
        'voltage': round(random.uniform(115.0, 125.0), 1),
        'cpu_usage': round(random.uniform(20.0, 80.0), 1),
        'memory_usage': round(random.uniform(30.0, 70.0), 1)
    }

def send_kiosk_data():
    """Enviar datos del kiosk al servidor"""
    KIOSK_DATA['sensors_data'] = generate_sensor_data()
    KIOSK_DATA['last_connection'] = datetime.utcnow().isoformat()
    
    try:
        # Actualizar datos en la base de datos
        app = create_app()
        with app.app_context():
            kiosk = Kiosk.query.get(KIOSK_DATA['id'])
            if kiosk:
                kiosk.status = 'online'
                kiosk.last_connection = datetime.utcnow()
                kiosk.update_sensor_data(KIOSK_DATA['sensors_data'])
                
                # Registrar log
                KioskLog.log_event(
                    kiosk_id=kiosk.id,
                    event_type='info',
                    message='Actualización de datos de sensores',
                    details=KIOSK_DATA['sensors_data']
                )
                
                db.session.commit()
        
        # Enviar datos vía WebSocket
        sio.emit('kiosk_update', {
            'kiosk_id': KIOSK_DATA['id'],
            'data': KIOSK_DATA
        })
        print(f'Datos enviados: {json.dumps(KIOSK_DATA["sensors_data"], indent=2)}')
    except Exception as e:
        print(f'Error al enviar datos: {str(e)}')

def main():
    try:
        # Conectar al servidor WebSocket
        sio.connect('http://localhost:5000')
        
        # Bucle principal
        while True:
            send_kiosk_data()
            time.sleep(5)  # Esperar 5 segundos entre actualizaciones
            
    except KeyboardInterrupt:
        print('\nDeteniendo simulador...')
        # Marcar kiosk como offline antes de salir
        app = create_app()
        with app.app_context():
            kiosk = Kiosk.query.get(KIOSK_DATA['id'])
            if kiosk:
                kiosk.status = 'offline'
                db.session.commit()
        
        sio.disconnect()
    except Exception as e:
        print(f'Error: {str(e)}')
        if sio.connected:
            sio.disconnect()

if __name__ == '__main__':
    main() 