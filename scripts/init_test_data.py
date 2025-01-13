"""Script para inicializar datos de prueba"""
import sys
import os
from datetime import datetime, UTC

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.extensions import db
from app.models import State, Location, Settings

def init_states():
    """Inicializar estados básicos"""
    states = [
        {'name': 'Normal', 'description': 'Funcionamiento normal', 'color_class': 'success'},
        {'name': 'Warning', 'description': 'Advertencias activas', 'color_class': 'warning'},
        {'name': 'Error', 'description': 'Errores críticos', 'color_class': 'danger'},
        {'name': 'Offline', 'description': 'Sin conexión', 'color_class': 'secondary'},
        {'name': 'Maintenance', 'description': 'En mantenimiento', 'color_class': 'info'}
    ]
    
    for state_data in states:
        if not State.query.filter_by(name=state_data['name']).first():
            state = State(**state_data)
            db.session.add(state)
    db.session.commit()
    print("Estados inicializados")

def init_locations():
    """Inicializar ubicaciones de prueba"""
    locations = [
        # Buenos Aires Centro
        {
            'name': 'Shopping Abasto',
            'address': 'Av. Corrientes 3247, CABA',
            'latitude': -34.6037,
            'longitude': -58.3816,
            'description': 'Centro comercial principal'
        },
        {
            'name': 'Terminal Retiro',
            'address': 'Av. Antártida Argentina s/n, CABA',
            'latitude': -34.5891,
            'longitude': -58.3738,
            'description': 'Terminal de buses principal'
        },
        # Córdoba
        {
            'name': 'Patio Olmos',
            'address': 'Av. Vélez Sarsfield 361, Córdoba',
            'latitude': -31.4201,
            'longitude': -64.1888,
            'description': 'Shopping center céntrico'
        },
        # Rosario
        {
            'name': 'Alto Rosario',
            'address': 'Junín 501, Rosario',
            'latitude': -32.9468,
            'longitude': -60.6393,
            'description': 'Centro comercial principal'
        },
        # Mendoza
        {
            'name': 'Mendoza Plaza',
            'address': 'Av. Acceso Este 3280, Guaymallén',
            'latitude': -32.8908,
            'longitude': -68.8272,
            'description': 'Shopping principal de Mendoza'
        }
    ]
    
    for loc_data in locations:
        if not Location.query.filter_by(name=loc_data['name']).first():
            location = Location(**loc_data)
            db.session.add(location)
    db.session.commit()
    print("Ubicaciones inicializadas")

def init_settings():
    """Inicializar configuraciones del sistema"""
    Settings.initialize_defaults()
    print("Configuraciones inicializadas")

def main():
    """Función principal"""
    app = create_app()
    with app.app_context():
        print("Inicializando datos de prueba...")
        init_states()
        init_locations()
        init_settings()
        print("Datos de prueba inicializados correctamente")

if __name__ == '__main__':
    main() 