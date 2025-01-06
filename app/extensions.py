from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

db = SQLAlchemy()
migrate = Migrate()
socketio = SocketIO(async_mode='threading')
cache = Cache()
limiter = Limiter(key_func=get_remote_address)

def init_extensions(app):
    """Inicializa todas las extensiones"""
    db.init_app(app)
    migrate.init_app(app, db)
    socketio.init_app(app, cors_allowed_origins="*")
    cache.init_app(app)
    limiter.init_app(app) 