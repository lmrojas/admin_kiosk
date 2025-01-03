from app import create_app, db
from app.models.kiosk import Kiosk

def init_test_kiosk():
    """Inicializar un kiosk de prueba"""
    app = create_app()
    with app.app_context():
        # Verificar si ya existe un kiosk de prueba
        kiosk = Kiosk.query.filter_by(serial_number='TEST001').first()
        if not kiosk:
            kiosk = Kiosk(
                serial_number='TEST001',
                name='Kiosk de Prueba',
                location_text='Ubicación de Prueba',
                ip_address='192.168.1.100',
                status='offline',
                state_id=1  # Estado normal
            )
            db.session.add(kiosk)
            db.session.commit()
            print("Kiosk de prueba creado exitosamente")
        else:
            print("El kiosk de prueba ya existe")

if __name__ == '__main__':
    init_test_kiosk() 