from app import create_app, db
from app.models.settings import Settings

def init_settings():
    """Inicializar configuraciones por defecto"""
    default_settings = {
        'system_name': 'Admin Kiosk',
        'refresh_interval': '5',
        'max_logs': '100',
        'cpu_warning': '80',
        'cpu_critical': '90',
        'ram_warning': '85',
        'ram_critical': '95',
        'disk_warning': '85',
        'disk_critical': '95'
    }
    
    for key, value in default_settings.items():
        Settings.set_value(key, value)
    
    print("Configuraciones inicializadas")

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        init_settings() 