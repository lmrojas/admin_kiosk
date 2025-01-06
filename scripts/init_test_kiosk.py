from app import create_app, db
from app.models.kiosk import Kiosk
import argparse
import random

def init_test_kiosks(num_kiosks=1):
    """Inicializar kiosks de prueba"""
    app = create_app()
    with app.app_context():
        kiosks_creados = 0
        for i in range(num_kiosks):
            serial = f'TEST{(i+1):03d}'
            # Verificar si ya existe el kiosk
            kiosk = Kiosk.query.filter_by(serial_number=serial).first()
            if not kiosk:
                # Generar IP aleatoria en el rango 192.168.1.x
                ip = f'192.168.1.{random.randint(100, 200)}'
                kiosk = Kiosk(
                    serial_number=serial,
                    name=f'Kiosk de Prueba {i+1}',
                    location_text=f'Ubicación de Prueba {i+1}',
                    ip_address=ip,
                    status='offline',
                    state_id=1  # Estado normal
                )
                db.session.add(kiosk)
                kiosks_creados += 1
        
        if kiosks_creados > 0:
            db.session.commit()
            print(f"{kiosks_creados} kiosks de prueba creados exitosamente")
        else:
            print("No se crearon nuevos kiosks (ya existían)")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--num_kiosks', type=int, default=1, help='Número de kiosks a crear')
    args = parser.parse_args()
    init_test_kiosks(args.num_kiosks) 