import sys
import os
import random
from datetime import datetime, timedelta
from faker import Faker

# Agregar el directorio raíz al path para poder importar la app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.extensions import db
from app.models.location import Location
from app.models.kiosk import Kiosk
from app.models.state import State

fake = Faker('es_ES')

def generate_locations():
    """Genera ubicaciones de prueba"""
    # Coordenadas base (Buenos Aires)
    base_lat = -34.6037
    base_lng = -58.3816
    
    locations = []
    for i in range(10):
        # Generar coordenadas cercanas a la base
        lat = base_lat + random.uniform(-0.1, 0.1)
        lng = base_lng + random.uniform(-0.1, 0.1)
        
        location = Location(
            name=f"Sucursal {fake.city()}",
            address=fake.street_address(),
            latitude=lat,
            longitude=lng,
            description=fake.text(max_nb_chars=200)
        )
        db.session.add(location)
    
    db.session.commit()
    return Location.query.all()

def generate_kiosks(locations):
    """Genera kiosks de prueba con ubicaciones asignadas y reales"""
    states = ['online', 'offline', 'maintenance']
    
    for i in range(124):
        # Seleccionar ubicación asignada
        location = random.choice(locations)
        
        # Generar coordenadas reales (con probabilidad de discrepancia)
        if random.random() < 0.2:  # 20% de probabilidad de discrepancia
            # Generar coordenadas significativamente diferentes
            current_lat = location.latitude + random.uniform(-0.01, 0.01)
            current_lng = location.longitude + random.uniform(-0.01, 0.01)
        else:
            # Generar coordenadas muy cercanas (dentro del margen aceptable)
            current_lat = location.latitude + random.uniform(-0.00005, 0.00005)
            current_lng = location.longitude + random.uniform(-0.00005, 0.00005)
        
        # Generar datos de sensores aleatorios
        sensors_data = {
            'cpu_usage': random.uniform(20, 95),
            'ram_usage': random.uniform(30, 98),
            'disk_usage': random.uniform(40, 99),
            'temperature': random.uniform(25, 45),
            'network': {
                'latency': random.uniform(50, 200),
                'bandwidth': random.uniform(10, 100)
            },
            'ups': {
                'status': random.choice(['line', 'battery']),
                'battery_level': random.uniform(20, 100),
                'estimated_runtime': random.randint(10, 120)
            }
        }
        
        # Crear kiosk
        kiosk = Kiosk(
            name=f"Kiosk {i+1:03d}",
            serial_number=f"SN{fake.unique.random_number(digits=8)}",
            status=random.choice(states),
            ip_address=fake.ipv4(),
            location_id=location.id,
            current_latitude=current_lat,
            current_longitude=current_lng,
            last_connection=datetime.utcnow() - timedelta(minutes=random.randint(0, 1440)),
            sensors_data=sensors_data
        )
        
        # Verificar discrepancia de ubicación
        kiosk.check_location_mismatch()
        db.session.add(kiosk)
        
        # Commit cada 10 kiosks para evitar sobrecarga de memoria
        if i % 10 == 0:
            db.session.commit()
    
    # Commit final
    db.session.commit()

def main():
    """Función principal para generar datos de prueba"""
    app = create_app()
    with app.app_context():
        try:
            # Limpiar datos existentes
            print("Limpiando datos existentes...")
            Kiosk.query.delete()
            Location.query.delete()
            db.session.commit()
            
            # Generar y guardar ubicaciones
            print("Generando ubicaciones...")
            locations = generate_locations()
            print(f"- {len(locations)} ubicaciones creadas")
            
            # Generar y guardar kiosks
            print("Generando kiosks...")
            generate_kiosks(locations)
            print(f"- 124 kiosks creados")
            
            print("Datos de prueba generados exitosamente!")
            
        except Exception as e:
            print(f"Error generando datos de prueba: {str(e)}")
            db.session.rollback()
            raise

if __name__ == '__main__':
    main() 