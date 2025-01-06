# Este archivo hace que el directorio blueprints sea un paquete Python
from app.blueprints.main import bp as main_bp
from app.blueprints.kiosk import bp as kiosks_bp
from app.blueprints.location import bp as location_bp

def init_blueprints(app):
    """Inicializa todos los blueprints de la aplicación"""
    app.register_blueprint(main_bp)
    app.register_blueprint(kiosks_bp, url_prefix='/kiosk')
    app.register_blueprint(location_bp, url_prefix='/location')
    app.logger.info('Blueprints registrados') 