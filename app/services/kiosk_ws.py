from flask_socketio import emit, join_room, leave_room
from app import socketio, db
from app.models.kiosk import Kiosk
from app.models.kiosk_log import KioskLog
from datetime import datetime
import json

@socketio.on('connect')
def handle_connect():
    """Manejar conexión de cliente"""
    emit('connect', {'data': 'Conectado al servidor'})

@socketio.on('disconnect')
def handle_disconnect():
    """Manejar desconexión de cliente"""
    pass

@socketio.on('join')
def handle_join(data):
    """Manejar unión a una sala de kiosk"""
    kiosk_id = data.get('kiosk_id')
    if kiosk_id:
        join_room(f'kiosk_{kiosk_id}')
        emit('join', {'data': f'Unido a la sala del kiosk {kiosk_id}'})

@socketio.on('leave')
def handle_leave(data):
    """Manejar salida de una sala de kiosk"""
    kiosk_id = data.get('kiosk_id')
    if kiosk_id:
        leave_room(f'kiosk_{kiosk_id}')
        emit('leave', {'data': f'Salido de la sala del kiosk {kiosk_id}'})

@socketio.on('kiosk_update')
def handle_kiosk_update(data):
    """Manejar actualización de estado de kiosk"""
    try:
        kiosk_id = data.get('kiosk_id')
        sensors_data = data.get('sensors_data')
        
        if not kiosk_id or not sensors_data:
            raise ValueError('Se requiere kiosk_id y sensors_data')
        
        kiosk = Kiosk.query.get(kiosk_id)
        if not kiosk:
            raise ValueError(f'Kiosk {kiosk_id} no encontrado')
        
        # Actualizar datos del kiosk
        kiosk.last_connection = datetime.utcnow()
        kiosk.update_sensor_data(sensors_data)
        
        # Registrar actualización en el log
        KioskLog.log_event(
            kiosk_id=kiosk.id,
            event_type='update',
            message='Actualización de sensores recibida',
            details=sensors_data
        )
        
        # Emitir actualización a todos los clientes en la sala del kiosk
        emit('kiosk_update', kiosk.to_dict(), room=f'kiosk_{kiosk_id}')
        
        db.session.commit()
        
    except Exception as e:
        db.session.rollback()
        emit('error', {'message': str(e)})

@socketio.on('execute_action')
def handle_execute_action(data):
    """Manejar ejecución de acción en kiosk"""
    try:
        kiosk_id = data.get('kiosk_id')
        action_id = data.get('action_id')
        
        if not kiosk_id or not action_id:
            raise ValueError('Se requiere kiosk_id y action_id')
        
        kiosk = Kiosk.query.get(kiosk_id)
        if not kiosk:
            raise ValueError(f'Kiosk {kiosk_id} no encontrado')
        
        # Aquí iría la lógica para ejecutar la acción en el kiosk
        # Por ahora solo registramos el intento
        
        # Registrar acción en el log
        KioskLog.log_event(
            kiosk_id=kiosk.id,
            event_type='action',
            message=f'Acción {action_id} ejecutada',
            details={'action_id': action_id}
        )
        
        # Emitir confirmación a todos los clientes en la sala del kiosk
        emit('action_executed', {
            'kiosk_id': kiosk_id,
            'action_id': action_id,
            'status': 'success'
        }, room=f'kiosk_{kiosk_id}')
        
        db.session.commit()
        
    except Exception as e:
        db.session.rollback()
        emit('error', {'message': str(e)}) 