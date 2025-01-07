import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime

def setup_logger(app):
    """Configura el sistema de logging"""
    if not os.path.exists('logs'):
        os.makedirs('logs')
        
    # Configurar el manejador de archivos
    file_handler = RotatingFileHandler(
        'logs/admin_kiosk.log',
        maxBytes=1024 * 1024,  # 1MB
        backupCount=10,
        delay=True  # No abrir el archivo hasta que sea necesario
    )
    file_handler.setFormatter(logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    ))
    file_handler.setLevel(logging.INFO)
    
    # Limpiar handlers existentes
    app.logger.handlers = []
    
    # Agregar handlers
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    
    app.logger.info('Admin Kiosk startup') 