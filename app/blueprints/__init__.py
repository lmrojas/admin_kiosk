# Este archivo hace que el directorio blueprints sea un paquete Python
from app.blueprints.main import bp as main_bp
from app.blueprints.kiosk import bp as kiosks_bp
from app.blueprints.location import bp as location_bp

def init_blueprints(app):
    """Inicializa todos los blueprints de la aplicación"""
    # Blueprint principal - sin prefijo
    app.register_blueprint(main_bp)
    
    # Blueprint de kiosks - prefijo /kiosk
    app.register_blueprint(kiosks_bp, url_prefix='/kiosk')
    
    # Blueprint de locations - prefijo /location
    app.register_blueprint(location_bp, url_prefix='/location')
    
    # Registrar rutas de error personalizadas
    register_error_handlers(app)

def register_error_handlers(app):
    """Registra los manejadores de error personalizados"""
    @app.errorhandler(404)
    def not_found_error(error):
        return {'error': 'Recurso no encontrado'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f'Error del servidor: {error}')
        return {'error': 'Error interno del servidor'}, 500
    
    @app.errorhandler(403)
    def forbidden_error(error):
        return {'error': 'Acceso denegado'}, 403 