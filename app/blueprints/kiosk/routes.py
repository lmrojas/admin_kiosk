from flask import render_template, jsonify, request, current_app
from app.blueprints.kiosk import bp
from app.models.kiosk import Kiosk
from app.models.state import State
from app.models.location import Location
from app.models.kiosk_location import KioskLocation
from app.models.kiosk_log import KioskLog
from app.models.settings import Settings
from app.extensions import db
from datetime import datetime

@bp.route('/')
def index():
    """Vista principal de kiosks"""
    current_app.logger.info('Accediendo a la vista de kiosks')
    kiosks = Kiosk.query.all()
    states = State.query.all()
    locations = Location.query.all()
    return render_template('kiosk/index.html', 
                         kiosks=kiosks,
                         states=states,
                         locations=locations)

@bp.route('/<int:id>')
def detail(id):
    """Vista detallada de un kiosk"""
    current_app.logger.info(f'Accediendo a detalles del kiosk {id}')
    kiosk = Kiosk.query.get_or_404(id)
    logs = KioskLog.query.filter_by(kiosk_id=id).order_by(KioskLog.created_at.desc()).limit(50).all()
    locations = Location.query.all()
    history = KioskLocation.query.filter_by(kiosk_id=id).order_by(KioskLocation.start_date.desc()).all()
    
    return render_template('kiosk/detail.html',
                         kiosk=kiosk,
                         logs=logs,
                         locations=locations,
                         history=history)

@bp.route('/logs')
def logs():
    """Vista de logs de kiosks"""
    current_app.logger.info('Accediendo a la vista de logs')
    logs = KioskLog.query.order_by(KioskLog.created_at.desc()).limit(100).all()
    return render_template('kiosk/logs.html', logs=logs)

@bp.route('/settings')
def settings():
    """Vista de configuración de kiosks"""
    current_app.logger.info('Accediendo a la vista de configuración')
    settings = Settings.query.all()
    return render_template('kiosk/settings.html', settings=settings)

@bp.route('/api/list')
def api_list():
    """API para listar kiosks con filtros"""
    current_app.logger.info('Solicitando lista de kiosks vía API')
    
    # Obtener parámetros de filtrado
    status = request.args.get('status')
    location_id = request.args.get('location_id')
    state_id = request.args.get('state_id')
    
    # Construir query base
    query = Kiosk.query
    
    # Aplicar filtros
    if status:
        query = query.filter(Kiosk.status == status)
    if location_id:
        query = query.filter(Kiosk.location_id == location_id)
    if state_id:
        query = query.filter(Kiosk.state_id == state_id)
    
    # Ejecutar query
    kiosks = query.all()
    return jsonify([k.to_dict() for k in kiosks])

@bp.route('/api/update/<int:kiosk_id>', methods=['POST'])
def api_update(kiosk_id):
    """API para actualizar un kiosk"""
    current_app.logger.info(f'Actualizando kiosk {kiosk_id}')
    
    kiosk = Kiosk.query.get_or_404(kiosk_id)
    data = request.get_json()
    
    try:
        if 'location_id' in data:
            kiosk.location_id = data['location_id']
        if 'state_id' in data:
            kiosk.state_id = data['state_id']
            
        db.session.commit()
        current_app.logger.info(f'Kiosk {kiosk_id} actualizado exitosamente')
        return jsonify({'status': 'success'})
        
    except Exception as e:
        current_app.logger.error(f'Error actualizando kiosk {kiosk_id}: {str(e)}')
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500 