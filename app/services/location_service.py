"""Servicio para manejar la lógica de ubicaciones"""
from datetime import datetime
from app.models.kiosk_location import KioskLocation
from app.extensions import db

class LocationService:
    # Margen de error aceptable en grados (aproximadamente 11 metros)
    LOCATION_MARGIN = 0.0001
    
    @staticmethod
    def check_location_mismatch(current_lat, current_lon, assigned_lat, assigned_lon):
        """
        Verifica si hay discrepancia entre la ubicación actual y la asignada
        """
        if None in (current_lat, current_lon, assigned_lat, assigned_lon):
            return False
            
        lat_diff = abs(assigned_lat - current_lat)
        lon_diff = abs(assigned_lon - current_lon)
        
        return lat_diff > LocationService.LOCATION_MARGIN or lon_diff > LocationService.LOCATION_MARGIN
    
    @staticmethod
    def register_location_change(kiosk, new_location, notes=None):
        """
        Registra un cambio de ubicación en el historial
        """
        # Cerrar el registro anterior si existe
        current_history = KioskLocation.query.filter_by(
            kiosk_id=kiosk.id,
            end_date=None
        ).first()
        
        if current_history:
            current_history.end_date = datetime.utcnow()
        
        # Crear nuevo registro
        new_history = KioskLocation(
            kiosk_id=kiosk.id,
            location_id=new_location.id,
            start_date=datetime.utcnow(),
            notes=notes
        )
        
        db.session.add(new_history)
        
        # Actualizar ubicación del kiosk
        kiosk.location = new_location
        
        try:
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def get_location_history(kiosk_id, limit=10):
        """
        Obtiene el historial de ubicaciones de un kiosk
        """
        return KioskLocation.query.filter_by(kiosk_id=kiosk_id)\
            .order_by(KioskLocation.start_date.desc())\
            .limit(limit)\
            .all() 