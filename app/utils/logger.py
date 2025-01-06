import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logger(app):
    """Configura el sistema de logging"""
    if not os.path.exists('logs'):
        os.mkdir('logs')
    
    # Configurar el logger principal
    file_handler = RotatingFileHandler('logs/admin_kiosk.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    
    # Configurar nivel de logging
    app.logger.setLevel(logging.INFO)
    app.logger.info('Admin Kiosk startup') 