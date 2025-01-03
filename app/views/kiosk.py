from flask import Blueprint, render_template, jsonify, request, current_app, abort
from app.models.kiosk import Kiosk
from app.models.state import State
from app.models.action import Action
from app.models.kiosk_log import KioskLog
from app import db, cache
from datetime import datetime
import json

bp = Blueprint('kiosk', __name__, url_prefix='/kiosk')

@bp.route('/')
@cache.cached(timeout=30)
def index():
    """Vista principal que muestra todos los kiosks"""
    kiosks = Kiosk.query.all()
    states = State.query.all()
    actions = Action.query.filter_by(is_active=True).all()
    return render_template('kiosk/index.html', kiosks=kiosks, states=states, actions=actions)

@bp.route('/<int:id>')
def detail(id):
    """Vista detallada de un kiosk específico"""
    kiosk = Kiosk.query.get_or_404(id)
    # Obtener los últimos 50 logs ordenados por fecha
    logs = KioskLog.query.filter_by(kiosk_id=id).order_by(KioskLog.created_at.desc()).limit(50).all()
    actions = Action.query.filter_by(is_active=True).all()
    return render_template('kiosk/detail.html', kiosk=kiosk, logs=logs, actions=actions)

@bp.route('/api/execute/<int:kiosk_id>/<int:action_id>', methods=['POST'])
def execute_action(kiosk_id, action_id):
    """Endpoint para ejecutar una acción en un kiosk"""
    kiosk = Kiosk.query.get_or_404(kiosk_id)
    action = Action.query.get_or_404(action_id)
    
    # Registrar la acción en el log
    KioskLog.log_event(
        kiosk_id=kiosk.id,
        event_type='action',
        message=f'Ejecutando acción: {action.name}',
        details={'action_id': action.id, 'command': action.command}
    )
    
    # Aquí se enviaría el comando al kiosk vía WebSocket
    # Por ahora solo actualizamos el estado
    kiosk.last_action_state = f'Executing {action.name}'
    db.session.commit()
    
    return jsonify({'success': True, 'message': f'Acción {action.name} iniciada'})

@bp.route('/api/logs/<int:kiosk_id>')
def get_logs(kiosk_id):
    """Endpoint para obtener los logs de un kiosk"""
    kiosk = Kiosk.query.get_or_404(kiosk_id)
    logs = kiosk.logs.order_by(KioskLog.created_at.desc()).limit(50).all()
    return jsonify([log.to_dict() for log in logs])

@bp.route('/api/add', methods=['POST'])
def add_kiosk():
    """Endpoint para agregar un nuevo kiosk"""
    data = request.get_json()
    
    if not data or not data.get('serial_number') or not data.get('name'):
        abort(400, description="Se requieren los campos serial_number y name")
    
    kiosk = Kiosk(
        serial_number=data['serial_number'],
        name=data['name'],
        location_text=data.get('location_text'),
        ip_address=data.get('ip_address')
    )
    
    db.session.add(kiosk)
    db.session.commit()
    
    return jsonify({
        'message': 'Kiosk creado exitosamente',
        'kiosk': kiosk.to_dict()
    }), 201 

@bp.route('/logs')
def logs():
    """Vista que muestra todos los logs"""
    kiosks = Kiosk.query.all()
    logs = KioskLog.query.order_by(KioskLog.created_at.desc()).limit(100).all()
    error_count = KioskLog.query.filter_by(event_type='error').count()
    warning_count = KioskLog.query.filter_by(event_type='warning').count()
    
    # Calcular eventos por hora
    total_logs = KioskLog.query.count()
    first_log = KioskLog.query.order_by(KioskLog.created_at.asc()).first()
    if first_log:
        hours_since_first = (datetime.utcnow() - first_log.created_at).total_seconds() / 3600
        events_per_hour = total_logs / hours_since_first if hours_since_first > 0 else 0
    else:
        events_per_hour = 0
    
    return render_template('kiosk/logs.html', 
                         logs=logs, 
                         kiosks=kiosks,
                         error_count=error_count,
                         warning_count=warning_count,
                         events_per_hour=round(events_per_hour, 1)) 

@bp.route('/settings')
def settings():
    """Vista para la configuración del sistema"""
    kiosks = Kiosk.query.all()
    states = State.query.all()
    actions = Action.query.filter_by(is_active=True).all()
    return render_template('kiosk/settings.html', 
                         kiosks=kiosks,
                         states=states, 
                         actions=actions) 