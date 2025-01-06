from flask import Blueprint, render_template, jsonify, request, current_app, abort
from app.models.kiosk import Kiosk
from app.models.state import State
from app.models.action import Action
from app.models.kiosk_log import KioskLog
from app.models.location import KioskLocation
from app import db, cache
from datetime import datetime
import json
from app.models.settings import Settings
from app.models.location import Location

bp = Blueprint('kiosk', __name__, url_prefix='/kiosk')

@bp.route('/')
def index():
    """Vista principal que muestra todos los kiosks"""
    kiosks = Kiosk.query.all()
    states = State.query.all()
    actions = Action.query.filter_by(is_active=True).all()
    locations = Location.query.all()
    return render_template('kiosk/index.html', 
                         kiosks=kiosks, 
                         states=states, 
                         actions=actions,
                         locations=locations)

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
    
    # Obtener configuración actual
    settings = {
        'system_name': Settings.get_value('system_name', 'Admin Kiosk'),
        'refresh_interval': int(Settings.get_value('refresh_interval', 5)),
        'max_logs': int(Settings.get_value('max_logs', 100)),
        'cpu_warning': int(Settings.get_value('cpu_warning', 80)),
        'cpu_critical': int(Settings.get_value('cpu_critical', 90)),
        'ram_warning': int(Settings.get_value('ram_warning', 85)),
        'ram_critical': int(Settings.get_value('ram_critical', 95)),
        'disk_warning': int(Settings.get_value('disk_warning', 85)),
        'disk_critical': int(Settings.get_value('disk_critical', 95))
    }
    
    return render_template('kiosk/settings.html', 
                         kiosks=kiosks,
                         states=states, 
                         actions=actions,
                         settings=settings) 

@bp.route('/api/action/<int:id>', methods=['GET'])
def get_action(id):
    """Obtener detalles de una acción"""
    action = Action.query.get_or_404(id)
    return jsonify({
        'id': action.id,
        'name': action.name,
        'command': action.command,
        'icon': action.icon,
        'requires_confirmation': action.requires_confirmation
    })

@bp.route('/api/action/<int:id>', methods=['DELETE'])
def delete_action(id):
    """Eliminar una acción"""
    action = Action.query.get_or_404(id)
    db.session.delete(action)
    db.session.commit()
    return jsonify({'success': True})

@bp.route('/api/action', methods=['POST'])
def create_action():
    """Crear o actualizar una acción"""
    data = request.get_json()
    
    if 'id' in data:
        action = Action.query.get_or_404(data['id'])
    else:
        action = Action()
        db.session.add(action)
    
    action.name = data['name']
    action.command = data['command']
    action.icon = data.get('icon', 'fas fa-cog')
    action.requires_confirmation = data.get('requires_confirmation', False)
    
    db.session.commit()
    return jsonify({'success': True})

@bp.route('/api/state/<int:id>', methods=['GET'])
def get_state(id):
    """Obtener detalles de un estado"""
    state = State.query.get_or_404(id)
    return jsonify({
        'id': state.id,
        'name': state.name,
        'color': state.color,
        'description': state.description
    })

@bp.route('/api/state/<int:id>', methods=['DELETE'])
def delete_state(id):
    """Eliminar un estado"""
    state = State.query.get_or_404(id)
    db.session.delete(state)
    db.session.commit()
    return jsonify({'success': True})

@bp.route('/api/state', methods=['POST'])
def create_state():
    """Crear o actualizar un estado"""
    data = request.get_json()
    
    if 'id' in data:
        state = State.query.get_or_404(data['id'])
    else:
        state = State()
        db.session.add(state)
    
    state.name = data['name']
    state.color = data['color']
    state.description = data.get('description', '')
    
    db.session.commit()
    return jsonify({'success': True})

@bp.route('/api/settings/general', methods=['POST'])
def update_general_settings():
    """Actualizar configuración general"""
    data = request.get_json()
    
    Settings.set_value('system_name', data.get('system_name', 'Admin Kiosk'))
    Settings.set_value('refresh_interval', str(data.get('refresh_interval', 5)))
    Settings.set_value('max_logs', str(data.get('max_logs', 100)))
    
    return jsonify({'success': True})

@bp.route('/api/settings/alerts', methods=['POST'])
def update_alert_settings():
    """Actualizar configuración de alertas"""
    data = request.get_json()
    
    Settings.set_value('cpu_warning', str(data.get('cpu_warning', 80)))
    Settings.set_value('cpu_critical', str(data.get('cpu_critical', 90)))
    Settings.set_value('ram_warning', str(data.get('ram_warning', 85)))
    Settings.set_value('ram_critical', str(data.get('ram_critical', 95)))
    Settings.set_value('disk_warning', str(data.get('disk_warning', 85)))
    Settings.set_value('disk_critical', str(data.get('disk_critical', 95)))
    
    return jsonify({'success': True})

@bp.route('/api/filter', methods=['GET'])
def filter_kiosks():
    """Endpoint para filtrar kiosks"""
    try:
        # Obtener parámetros de filtrado
        status = request.args.getlist('status[]')  # Lista de estados seleccionados
        location_id = request.args.get('location')
        alert_level = request.args.get('alert')
        search = request.args.get('search')
        
        # Construir query base
        query = Kiosk.query
        
        # Aplicar filtros
        if status:
            query = query.filter(Kiosk.status.in_(status))
        
        if location_id and location_id.isdigit():
            query = query.filter(Kiosk.location_id == int(location_id))
        
        if search:
            search = f"%{search}%"
            query = query.filter(
                db.or_(
                    Kiosk.name.ilike(search),
                    Kiosk.serial_number.ilike(search)
                )
            )
        
        # Ejecutar query
        kiosks = query.all()
        
        # Filtrar por alert_level después de obtener los resultados
        if alert_level:
            kiosks = [k for k in kiosks if k.alert_level == alert_level]
        
        # Preparar datos para respuesta
        kiosks_data = []
        for kiosk in kiosks:
            try:
                sensors = kiosk.sensors_data_dict
                location_name = kiosk.location.name if kiosk.location else 'No asignada'
                
                kiosks_data.append({
                    'id': kiosk.id,
                    'status': kiosk.status or 'offline',
                    'name': kiosk.name,
                    'serial_number': kiosk.serial_number,
                    'location_id': kiosk.location_id,
                    'location': location_name,
                    'ip_address': kiosk.ip_address or 'N/A',
                    'cpu_usage': float(sensors.get('cpu_usage', 0)),
                    'ram_usage': float(sensors.get('ram_usage', 0)),
                    'disk_usage': float(sensors.get('disk_usage', 0)),
                    'temperature': float(sensors.get('temperature', 0)),
                    'alert_level': kiosk.alert_level or 'none',
                    'last_connection': kiosk.last_connection.strftime('%d/%m/%Y %H:%M:%S') if kiosk.last_connection else 'Nunca'
                })
            except (ValueError, AttributeError, TypeError) as e:
                current_app.logger.error(f"Error procesando kiosk {kiosk.id}: {str(e)}")
                continue
        
        return jsonify({
            'kiosks': kiosks_data,
            'total': len(kiosks_data)
        })
        
    except Exception as e:
        current_app.logger.error(f"Error en filter_kiosks: {str(e)}")
        return jsonify({
            'error': 'Error al filtrar los kiosks',
            'message': str(e)
        }), 500

@bp.route('/api/delete/<int:id>', methods=['DELETE'])
def delete_kiosk(id):
    """Eliminar un kiosk"""
    kiosk = Kiosk.query.get_or_404(id)
    
    # Eliminar registros relacionados
    KioskLog.query.filter_by(kiosk_id=id).delete()
    KioskLocation.query.filter_by(kiosk_id=id).delete()
    
    # Eliminar el kiosk
    db.session.delete(kiosk)
    db.session.commit()
    
    return jsonify({'success': True}) 