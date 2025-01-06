from app import create_app, db
from app.models.kiosk import Kiosk
from app.models.location import Location, KioskLocation
from app.models.state import State
from app.models.kiosk_log import KioskLog
from datetime import datetime, timedelta
import random
import time
import threading
import math

def generate_random_ip():
    return f"192.168.{random.randint(0, 255)}.{random.randint(1, 254)}"

def generate_random_serial():
    return f"KSK-{random.randint(1000, 9999)}-{random.randint(100, 999)}"

def create_initial_states():
    states = [
        {"name": "Operativo", "color_class": "success", "description": "Kiosk funcionando normalmente"},
        {"name": "Mantenimiento", "color_class": "warning", "description": "En mantenimiento programado"},
        {"name": "Error", "color_class": "danger", "description": "Presenta errores de funcionamiento"},
        {"name": "Reiniciando", "color_class": "info", "description": "En proceso de reinicio"},
        {"name": "Actualización", "color_class": "primary", "description": "Instalando actualizaciones"},
        {"name": "Suspendido", "color_class": "secondary", "description": "Temporalmente fuera de servicio"}
    ]
    
    for state_data in states:
        if not State.query.filter_by(name=state_data["name"]).first():
            state = State(**state_data)
            db.session.add(state)
    
    db.session.commit()
    return State.query.all()

def create_initial_locations():
    locations = [
        {"name": "Centro Comercial Plaza Mayor", "address": "Av. Principal 123"},
        {"name": "Terminal de Transporte Norte", "address": "Calle 45 #23-67"},
        {"name": "Aeropuerto Internacional", "address": "Zona Aeroportuaria"},
        {"name": "Estación Central Metro", "address": "Carrera 50 #10-15"},
        {"name": "Mall del Sur", "address": "Av. Sur #78-90"},
        {"name": "Plaza Central", "address": "Calle 15 #45-23"},
        {"name": "Centro Empresarial Torre Norte", "address": "Av. Empresarial 234"},
        {"name": "Terminal Sur", "address": "Autopista Sur Km 2"},
        {"name": "Centro Comercial Oasis", "address": "Calle 80 #65-43"},
        {"name": "Estación de Tren Central", "address": "Vía Férrea Principal"}
    ]
    
    for loc_data in locations:
        if not Location.query.filter_by(name=loc_data["name"]).first():
            location = Location(**loc_data)
            db.session.add(location)
    
    db.session.commit()
    return Location.query.all()

def create_kiosks(num_kiosks):
    states = create_initial_states()
    locations = create_initial_locations()
    
    kiosks = []
    for i in range(num_kiosks):
        # Generar estado inicial con probabilidades realistas
        initial_state = random.choices(
            states,
            weights=[70, 10, 5, 5, 5, 5],  # 70% operativos, resto distribuido
            k=1
        )[0]
        
        # Generar estado online/offline con 85% probabilidad de estar online
        initial_status = random.choices(['online', 'offline'], weights=[85, 15])[0]
        
        # Generar datos de sensores realistas
        sensors_data = {
            'cpu_usage': random.uniform(20, 95),
            'ram_usage': random.uniform(30, 90),
            'disk_usage': random.uniform(40, 95),
            'temperature': random.uniform(25, 42),
            'humidity': random.uniform(30, 70),
            'network': {
                'latency': random.randint(5, 200),
                'download_speed': random.uniform(1, 100),
                'upload_speed': random.uniform(1, 50),
                'signal_strength': random.uniform(20, 100)
            },
            'ups': {
                'status': random.choice(['online', 'battery', 'bypass']),
                'battery_level': random.uniform(60, 100),
                'estimated_runtime': random.randint(30, 120)
            }
        }
        
        kiosk = Kiosk(
            name=f"Kiosk {i+1:03d}",
            serial_number=generate_random_serial(),
            ip_address=generate_random_ip(),
            state_id=initial_state.id,
            status=initial_status,
            sensors_data=sensors_data,
            last_connection=datetime.utcnow() - timedelta(minutes=random.randint(0, 60))
        )
        db.session.add(kiosk)
        kiosks.append(kiosk)
    
    db.session.commit()
    
    # Asignar ubicaciones iniciales
    for kiosk in kiosks:
        location = random.choice(locations)
        kiosk_location = KioskLocation(
            kiosk_id=kiosk.id,
            location_id=location.id,
            start_date=datetime.utcnow() - timedelta(days=random.randint(1, 30))
        )
        db.session.add(kiosk_location)
    
    db.session.commit()
    return kiosks

def generate_event(kiosk, states):
    event_types = ['info', 'warning', 'error']
    messages = [
        "Actualización de software completada",
        "Reinicio programado ejecutado",
        "Error de conexión detectado",
        "Mantenimiento preventivo realizado",
        "Alerta de temperatura alta",
        "Cambio de estado detectado",
        "Conexión restablecida",
        "Problema de impresora detectado",
        "Nivel bajo de papel",
        "Error de lectura de tarjeta",
        "Fallo en sensor biométrico",
        "Problema en dispensador de efectivo",
        "Error en lector de tarjetas",
        "Fallo en impresora térmica",
        "Problema en pantalla táctil"
    ]
    
    event_type = random.choice(event_types)
    message = random.choice(messages)
    
    KioskLog.log_event(
        kiosk_id=kiosk.id,
        event_type=event_type,
        message=message,
        details={
            'sensors': kiosk.sensors_data,
            'state_id': kiosk.state_id,
            'timestamp': datetime.utcnow().isoformat()
        }
    )

def update_kiosk_status(kiosk, states, locations):
    # Actualizar métricas con variaciones realistas
    sensors_data = kiosk.sensors_data or {}
    
    # CPU: variación suave con picos ocasionales
    cpu_change = random.normalvariate(0, 3)  # Distribución normal
    if random.random() < 0.05:  # 5% de probabilidad de pico
        cpu_change = random.uniform(10, 30)
    sensors_data['cpu_usage'] = min(max(sensors_data.get('cpu_usage', 50) + cpu_change, 0), 100)
    
    # RAM: cambios más graduales
    ram_change = random.normalvariate(0, 2)
    sensors_data['ram_usage'] = min(max(sensors_data.get('ram_usage', 50) + ram_change, 0), 100)
    
    # Disco: cambios muy graduales
    disk_change = random.normalvariate(0, 1)
    sensors_data['disk_usage'] = min(max(sensors_data.get('disk_usage', 50) + disk_change, 0), 100)
    
    # Temperatura: variación basada en hora del día
    hour = datetime.now().hour
    base_temp = 25 + (5 * math.sin((hour - 6) * math.pi / 12))  # Pico a las 18h
    temp_change = random.normalvariate(0, 1)
    sensors_data['temperature'] = min(max(base_temp + temp_change, 20), 45)
    
    # Red: actualizar métricas de red
    network = sensors_data.get('network', {})
    network['latency'] = max(5, min(200, network.get('latency', 50) + random.normalvariate(0, 10)))
    network['download_speed'] = max(1, min(100, network.get('download_speed', 50) + random.normalvariate(0, 5)))
    network['upload_speed'] = max(1, min(50, network.get('upload_speed', 25) + random.normalvariate(0, 3)))
    network['signal_strength'] = max(20, min(100, network.get('signal_strength', 80) + random.normalvariate(0, 2)))
    sensors_data['network'] = network
    
    # UPS: actualizar estado de batería
    ups = sensors_data.get('ups', {})
    if ups.get('status') == 'battery':
        ups['battery_level'] = max(0, ups.get('battery_level', 100) - random.uniform(0.5, 2))
        ups['estimated_runtime'] = max(0, int(ups.get('estimated_runtime', 60) * 0.95))
    else:
        ups['battery_level'] = min(100, ups.get('battery_level', 90) + random.uniform(0, 0.5))
        ups['estimated_runtime'] = min(120, int(ups.get('estimated_runtime', 60) * 1.05))
    sensors_data['ups'] = ups
    
    kiosk.sensors_data = sensors_data
    
    # Actualizar estado online/offline (5% de probabilidad de cambiar)
    if random.random() < 0.05:
        new_status = random.choices(['online', 'offline'], weights=[80, 20])[0]
        if new_status != kiosk.status:
            kiosk.status = new_status
            if kiosk.status == 'offline':
                generate_event(kiosk, states)
                KioskLog.log_event(
                    kiosk_id=kiosk.id,
                    event_type='warning',
                    message='Kiosk desconectado',
                    details={'status': 'offline'}
                )
            else:
                KioskLog.log_event(
                    kiosk_id=kiosk.id,
                    event_type='info',
                    message='Kiosk conectado',
                    details={'status': 'online'}
                )
    
    # Cambiar estado con probabilidades realistas
    if random.random() < 0.1:  # 10% de probabilidad de cambio de estado
        weights = [70, 10, 5, 5, 5, 5]  # Mantener distribución realista
        new_state = random.choices(states, weights=weights)[0]
        if new_state.id != kiosk.state_id:
            kiosk.state_id = new_state.id
            generate_event(kiosk, states)
    
    # Cambiar ubicación (2% de probabilidad)
    if random.random() < 0.02:
        current_location = KioskLocation.query.filter_by(
            kiosk_id=kiosk.id,
            end_date=None
        ).first()
        
        if current_location:
            current_location.end_date = datetime.utcnow()
            
        new_location = random.choice(locations)
        kiosk_location = KioskLocation(
            kiosk_id=kiosk.id,
            location_id=new_location.id,
            start_date=datetime.utcnow()
        )
        db.session.add(kiosk_location)
        
        KioskLog.log_event(
            kiosk_id=kiosk.id,
            event_type='info',
            message=f'Kiosk reubicado a {new_location.name}',
            details={'location_id': new_location.id}
        )
    
    kiosk.last_connection = datetime.utcnow()
    db.session.commit()

def simulation_thread(app):
    with app.app_context():
        states = State.query.all()
        locations = Location.query.all()
        kiosks = Kiosk.query.all()
        
        while True:
            try:
                for kiosk in kiosks:
                    update_kiosk_status(kiosk, states, locations)
                    if random.random() < 0.2:  # 20% de probabilidad de generar un evento
                        generate_event(kiosk, states)
                time.sleep(5)  # Actualizar cada 5 segundos
            except Exception as e:
                print(f"Error en simulación: {e}")
                time.sleep(1)

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        # Limpiar datos existentes
        KioskLog.query.delete()
        KioskLocation.query.delete()
        Kiosk.query.delete()
        State.query.delete()
        Location.query.delete()
        db.session.commit()
        
        print("Generando datos iniciales...")
        kiosks = create_kiosks(45)  # Generar 45 kiosks
        print(f"Creados {len(kiosks)} kiosks")
        
        print("Iniciando simulación...")
        sim_thread = threading.Thread(target=simulation_thread, args=(app,))
        sim_thread.daemon = True
        sim_thread.start()
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nSimulación detenida por el usuario") 