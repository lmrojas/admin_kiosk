from app import create_app, db
from app.models.kiosk import Kiosk
from app.models.location import Location, KioskLocation
from app.models.state import State
from app.models.kiosk_log import KioskLog
from datetime import datetime, timedelta
import random
import time
import threading

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
        kiosk = Kiosk(
            name=f"Kiosk {i+1:03d}",
            serial_number=generate_random_serial(),
            ip_address=generate_random_ip(),
            state_id=random.choice(states).id,
            status='online',
            sensors_data={
                'cpu_usage': random.randint(10, 90),
                'ram_usage': random.randint(20, 85),
                'disk_usage': random.randint(30, 95)
            },
            last_connection=datetime.utcnow()
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
        "Error de lectura de tarjeta"
    ]
    
    event_type = random.choice(event_types)
    message = random.choice(messages)
    
    KioskLog.log_event(
        kiosk_id=kiosk.id,
        event_type=event_type,
        message=message,
        details={
            'sensors': kiosk.sensors_data,
            'state_id': kiosk.state_id
        }
    )

def update_kiosk_status(kiosk, states, locations):
    # Actualizar métricas
    sensors_data = kiosk.sensors_data or {}
    sensors_data['cpu_usage'] = min(max(sensors_data.get('cpu_usage', 50) + random.randint(-10, 10), 0), 100)
    sensors_data['ram_usage'] = min(max(sensors_data.get('ram_usage', 50) + random.randint(-5, 5), 0), 100)
    sensors_data['disk_usage'] = min(max(sensors_data.get('disk_usage', 50) + random.randint(-2, 2), 0), 100)
    kiosk.sensors_data = sensors_data
    
    # Actualizar estado online/offline (5% de probabilidad de cambiar)
    if random.random() < 0.05:
        kiosk.status = random.choices(['online', 'offline'], weights=[80, 20])[0]
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
    
    # Cambiar estado aleatoriamente (10% de probabilidad)
    if random.random() < 0.1:
        kiosk.state_id = random.choice(states).id
        generate_event(kiosk, states)
    
    # Cambiar ubicación aleatoriamente (5% de probabilidad)
    if random.random() < 0.05:
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
        kiosks = create_kiosks(124)
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