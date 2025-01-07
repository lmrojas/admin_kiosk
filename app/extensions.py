from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_mail import Mail

# Inicializar extensiones
db = SQLAlchemy()
migrate = Migrate()
socketio = SocketIO(async_mode='threading', cors_allowed_origins="*")
cache = Cache()
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)
mail = Mail()

def init_extensions(app):
    """Inicializa todas las extensiones"""
    # Base de datos y migraciones
    db.init_app(app)
    migrate.init_app(app, db)
    
    # WebSocket
    socketio.init_app(app)
    
    # Cache y rate limiting
    cache.init_app(app)
    limiter.init_app(app)
    
    # Email
    mail.init_app(app) 