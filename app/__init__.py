from flask import Flask
import os
from app.extensions import init_extensions, db
from app.utils.logger import setup_logger
from app.blueprints import init_blueprints

def create_app(config_name=None):
    """Crea y configura la aplicación Flask"""
    app = Flask(__name__)
    
    # Configuración por defecto
    app.config.update(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev-key-12345'),
        SQLALCHEMY_DATABASE_URI='postgresql://postgres:postgres@localhost/admin_kiosk',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        CACHE_TYPE='simple',
        CACHE_DEFAULT_TIMEOUT=300,
        JSON_SORT_KEYS=False,
        MAX_CONTENT_LENGTH=16 * 1024 * 1024,  # 16MB max-limit
        UPLOAD_FOLDER=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads'),
        LOG_DIR=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs')
    )
    
    # Asegurar que existan los directorios necesarios
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['LOG_DIR'], exist_ok=True)
    
    # Configurar logger
    setup_logger(app)
    app.logger.info('Iniciando aplicación Admin Kiosk')
    
    # Inicializar extensiones
    init_extensions(app)
    app.logger.info('Extensiones inicializadas')
    
    # Registrar blueprints
    init_blueprints(app)
    app.logger.info('Blueprints registrados')
    
    # Agregar filtros para las plantillas
    @app.template_filter('datetime')
    def format_datetime(value):
        if value is None:
            return 'Nunca'
        return value.strftime('%d/%m/%Y %H:%M:%S')
    
    # Importar modelos y crear tablas
    with app.app_context():
        app.logger.info('Inicializando modelos y tablas')
        # Importar todos los modelos para que SQLAlchemy los reconozca
        from app.models.kiosk import Kiosk
        from app.models.location import Location
        from app.models.state import State
        from app.models.action import Action
        from app.models.kiosk_log import KioskLog
        from app.models.settings import Settings
        from app.models.kiosk_location import KioskLocation
        
        # Crear todas las tablas
        db.create_all()
        app.logger.info('Tablas creadas')
        
        # Inicializar configuraciones por defecto
        Settings.initialize_defaults()
        app.logger.info('Configuraciones inicializadas')
    
    return app 

def register_blueprints(app):
    """Registrar blueprints"""
    from app.blueprints.main import bp as main_bp
    from app.blueprints.kiosk import bp as kiosk_bp
    from app.blueprints.location import bp as location_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(kiosk_bp, url_prefix='/kiosk')
    app.register_blueprint(location_bp, url_prefix='/location') 