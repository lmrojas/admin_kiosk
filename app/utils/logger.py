import logging
from logging.handlers import RotatingFileHandler
import os
from datetime import datetime
import socket
from typing import Dict, Optional

class CustomFormatter(logging.Formatter):
    """Formateador personalizado para logs con formato específico"""
    
    def format(self, record):
        record.hostname = socket.gethostname()
        if not hasattr(record, 'trace_id'):
            record.trace_id = 'no_trace'
        if not hasattr(record, 'extra_data'):
            record.extra_data = '{}'
        return super().format(record)

def setup_logger(name: str, log_file: str, level: int = logging.INFO) -> logging.Logger:
    """Configurar un logger específico con rotación de archivos"""
    
    # Crear directorio de logs si no existe
    log_dir = os.path.dirname(log_file)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Evitar duplicación de handlers
    if logger.handlers:
        return logger
    
    # Configurar handler con rotación
    handler = RotatingFileHandler(
        log_file,
        maxBytes=10485760,  # 10MB
        backupCount=10
    )
    
    # Formato detallado según documentación
    formatter = CustomFormatter(
        '%(asctime)s | %(hostname)s | %(name)s | %(levelname)s | %(message)s | '
        'trace_id=%(trace_id)s | %(extra_data)s'
    )
    
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger

# Crear loggers principales
LOGS_DIR = 'logs'
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

system_logger = setup_logger('system', os.path.join(LOGS_DIR, 'system.log'))
kiosk_logger = setup_logger('kiosk', os.path.join(LOGS_DIR, 'kiosk.log'))
websocket_logger = setup_logger('websocket', os.path.join(LOGS_DIR, 'websocket.log'))
actions_logger = setup_logger('actions', os.path.join(LOGS_DIR, 'actions.log'))
error_logger = setup_logger('error', os.path.join(LOGS_DIR, 'error.log'), level=logging.ERROR)

def log_event(
    logger: logging.Logger,
    message: str,
    level: int = logging.INFO,
    trace_id: Optional[str] = None,
    extra_data: Optional[Dict] = None
) -> None:
    """Función helper para logging con datos extra"""
    extra = {
        'trace_id': trace_id or 'no_trace',
        'extra_data': str(extra_data or {})
    }
    logger.log(level, message, extra=extra) 