from flask import render_template, current_app
from app.blueprints.main import bp
from app.models.kiosk import Kiosk
from app.models.location import Location
from app.models.state import State
from app.models.settings import Settings
from app.models.kiosk_log import KioskLog

@bp.route('/')
def index():
    """Vista del dashboard principal"""
    current_app.logger.info('Accediendo al dashboard principal')
    
    # Estadísticas para el dashboard
    stats = {
        'total_kiosks': Kiosk.query.count(),
        'online_kiosks': Kiosk.query.filter_by(status='online').count(),
        'offline_kiosks': Kiosk.query.filter_by(status='offline').count(),
        'total_locations': Location.query.count()
    }
    
    # Últimos kiosks actualizados
    kiosks = Kiosk.query.order_by(Kiosk.updated_at.desc()).limit(5).all()
    
    # Logs recientes
    recent_logs = KioskLog.query.order_by(KioskLog.created_at.desc()).limit(10).all()
    
    # Configuraciones del sistema
    settings = Settings.query.first()
    
    return render_template('main/index.html',
                         stats=stats,
                         kiosks=kiosks,
                         recent_logs=recent_logs,
                         settings=settings)

@bp.route('/settings')
def settings():
    """Vista de configuraciones"""
    current_app.logger.info('Accediendo a la vista de configuraciones')
    settings = Settings.query.all()
    return render_template('main/settings.html', settings=settings) 