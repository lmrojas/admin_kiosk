import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models.state import State
from app.models.action import Action
from app.models.kiosk import Kiosk
from app.models.location import Location, KioskLocation
from datetime import datetime

def init_db():
    """Inicializar la base de datos con datos de prueba"""
    app = create_app()
    with app.app_context():
        # Crear estados por defecto si no existen
        states = [
            {'name': 'Online', 'description': 'Kiosk conectado y funcionando', 'color_class': 'success'},
            {'name': 'Offline', 'description': 'Kiosk desconectado', 'color_class': 'danger'},
            {'name': 'Warning', 'description': 'Kiosk con advertencias', 'color_class': 'warning'},
            {'name': 'Maintenance', 'description': 'Kiosk en mantenimiento', 'color_class': 'info'}
        ]
        
        for state_data in states:
            state = State.query.filter_by(name=state_data['name']).first()
            if not state:
                state = State(**state_data)
                db.session.add(state)
                print(f'Estado creado: {state_data["name"]}')
            else:
                for key, value in state_data.items():
                    setattr(state, key, value)
                print(f'Estado actualizado: {state_data["name"]}')
        
        # Crear o actualizar acciones por defecto
        actions = [
            {
                'name': 'Reiniciar',
                'command': 'restart',
                'description': 'Reiniciar el kiosk',
                'icon_class': 'fas fa-sync',
                'requires_confirmation': True
            },
            {
                'name': 'Actualizar',
                'command': 'update',
                'description': 'Actualizar el software del kiosk',
                'icon_class': 'fas fa-download',
                'requires_confirmation': True
            },
            {
                'name': 'Limpiar Logs',
                'command': 'clean_logs',
                'description': 'Limpiar los logs del kiosk',
                'icon_class': 'fas fa-broom',
                'requires_confirmation': False
            }
        ]
        
        for action_data in actions:
            action = Action.query.filter_by(command=action_data['command']).first()
            if not action:
                action = Action(**action_data)
                db.session.add(action)
                print(f'Acción creada: {action_data["name"]}')
            else:
                for key, value in action_data.items():
                    setattr(action, key, value)
                print(f'Acción actualizada: {action_data["name"]}')
        
        # Crear ubicaciones de prueba si no existen
        locations = [
            {
                'name': 'Sucursal Centro',
                'description': 'Sucursal principal en el centro de la ciudad',
                'address': 'Av. Principal 123, Centro',
                'latitude': -34.603722,
                'longitude': -58.381592
            },
            {
                'name': 'Sucursal Norte',
                'description': 'Sucursal en zona norte',
                'address': 'Calle Norte 456',
                'latitude': -34.583722,
                'longitude': -58.391592
            }
        ]
        
        for location_data in locations:
            location = Location.query.filter_by(name=location_data['name']).first()
            if not location:
                location = Location(**location_data)
                db.session.add(location)
                print(f'Ubicación creada: {location_data["name"]}')
            else:
                for key, value in location_data.items():
                    setattr(location, key, value)
                print(f'Ubicación actualizada: {location_data["name"]}')
        
        # Guardar cambios para tener los IDs
        db.session.commit()
        
        # Crear kiosk de prueba si no existe
        kiosk = Kiosk.query.filter_by(serial_number='SIM001').first()
        if not kiosk:
            kiosk = Kiosk(
                serial_number='SIM001',
                name='Kiosk Simulado',
                location_text='Ubicación de prueba',
                ip_address='192.168.1.100',
                status='offline',
                sensors_data={
                    'temperature': 25.0,
                    'humidity': 50.0,
                    'voltage': 120.0,
                    'cpu_usage': 30.0,
                    'memory_usage': 45.0
                }
            )
            db.session.add(kiosk)
            db.session.commit()
            print(f'Kiosk creado: {kiosk.name}')
            
            # Asignar ubicación inicial
            location = Location.query.first()
            if location:
                kiosk_location = KioskLocation(
                    kiosk_id=kiosk.id,
                    location_id=location.id,
                    notes='Ubicación inicial'
                )
                db.session.add(kiosk_location)
                print(f'Ubicación asignada al kiosk: {location.name}')
        else:
            print(f'Kiosk ya existe: {kiosk.name}')
        
        # Guardar todos los cambios
        db.session.commit()
        print('Base de datos inicializada exitosamente')

if __name__ == '__main__':
    init_db() 