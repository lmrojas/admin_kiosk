from typing import Dict, Optional

class KioskError(Exception):
    """Clase base para excepciones del sistema de kiosks"""
    
    def __init__(self, message: str, error_code: Optional[str] = None, extra_data: Optional[Dict] = None):
        self.message = message
        self.error_code = error_code
        self.extra_data = extra_data or {}
        super().__init__(self.message)

class KioskConnectionError(KioskError):
    """Error de conexión con el kiosk"""
    pass

class KioskCommandError(KioskError):
    """Error al ejecutar un comando en el kiosk"""
    pass

class KioskValidationError(KioskError):
    """Error de validación de datos del kiosk"""
    pass

class WebSocketError(KioskError):
    """Error en la conexión WebSocket"""
    pass

class KioskAuthenticationError(KioskError):
    """Error de autenticación del kiosk"""
    pass

class KioskTimeoutError(KioskError):
    """Error de timeout en operación del kiosk"""
    pass

class KioskStateError(KioskError):
    """Error en el estado del kiosk"""
    pass 