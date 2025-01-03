from app import create_app, db
from app.models.kiosk import Kiosk
import random
import time
from datetime import datetime

def generate_sensor_data():
    """Generar datos aleatorios de sensores"""
    return {
        'cpu_usage': random.uniform(50, 95),
        'ram_usage': random.uniform(60, 98),
        'disk_usage': random.uniform(70, 98),
        'temperature': random.uniform(30, 45),
        'humidity': random.uniform(40, 80),
        'network': {
            'latency': random.randint(5, 200),
            'download_speed': random.uniform(1, 100),
            'upload_speed': random.uniform(1, 50),
            'signal_strength': random.uniform(20, 100)
        },
        'ups': {
            'status': random.choice(['online', 'battery', 'bypass']),
            'battery_level': random.uniform(5, 100),
            'estimated_runtime': random.randint(5, 120)
        },
        'errors': [],
        'warnings': []
    }

def test_sensors():
    """Probar actualización de sensores"""
    app = create_app()
    with app.app_context():
        # Obtener todos los kiosks
        kiosks = Kiosk.query.all()
        if not kiosks:
            print("No hay kiosks en la base de datos")
            return
        
        print(f"Iniciando simulación con {len(kiosks)} kiosks")
        try:
            while True:
                for kiosk in kiosks:
                    # Generar datos aleatorios
                    data = generate_sensor_data()
                    
                    # Agregar algunos errores y advertencias aleatorias
                    if random.random() < 0.2:  # 20% de probabilidad
                        data['errors'].append(random.choice([
                            'Error de conexión con impresora',
                            'Error de lectura en disco',
                            'Fallo en ventilador'
                        ]))
                    
                    if random.random() < 0.3:  # 30% de probabilidad
                        data['warnings'].append(random.choice([
                            'Papel bajo en impresora',
                            'Actualización pendiente',
                            'Rendimiento degradado'
                        ]))
                    
                    # Actualizar estado online/offline
                    kiosk.status = 'online' if random.random() > 0.1 else 'offline'
                    
                    # Actualizar datos de sensores
                    kiosk.update_sensor_data(data)
                    print(f"Kiosk {kiosk.name} actualizado - {datetime.now()}")
                
                # Esperar 5 segundos antes de la siguiente actualización
                time.sleep(5)
                
        except KeyboardInterrupt:
            print("\nSimulación detenida por el usuario")

if __name__ == '__main__':
    test_sensors() 