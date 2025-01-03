from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os

db = SQLAlchemy()
migrate = Migrate()
socketio = SocketIO(async_mode='threading')
cache = Cache()
limiter = Limiter(key_func=get_remote_address)

def create_app(config=None):
    app = Flask(__name__)
    
    # Configuración por defecto
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-12345')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///kiosk.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Sobreescribir con configuración personalizada
    if config:
        app.config.update(config)
    
    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    socketio.init_app(app, cors_allowed_origins="*")
    cache.init_app(app)
    limiter.init_app(app)
    
    # Importar modelos para que SQLAlchemy los reconozca
    from app.models.kiosk import Kiosk
    from app.models.location import Location, KioskLocation
    from app.models.state import State
    from app.models.action import Action
    from app.models.kiosk_log import KioskLog
    from app.models.user import User
    
    # Registrar blueprints
    from app.views import kiosk, location
    app.register_blueprint(kiosk.bp)
    app.register_blueprint(location.bp)
    
    # Ruta principal
    @app.route('/')
    def index():
        return kiosk.index()
    
    return app 