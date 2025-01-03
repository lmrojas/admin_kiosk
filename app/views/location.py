from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for, abort
from app import db
from app.models.location import Location, KioskLocation
from app.models.kiosk import Kiosk
from app import cache
from datetime import datetime

bp = Blueprint('location', __name__, url_prefix='/location')

@bp.route('/')
@cache.cached(timeout=30)
def index():
    """Vista principal que muestra todas las ubicaciones"""
    locations = Location.get_active_locations()
    return render_template('location/index.html', locations=locations)

@bp.route('/kiosk/<int:kiosk_id>')
def kiosk_history(kiosk_id):
    """Vista que muestra el historial de ubicaciones de un kiosk"""
    kiosk = Kiosk.query.get_or_404(kiosk_id)
    locations = Location.get_active_locations()
    history = KioskLocation.query.filter_by(kiosk_id=kiosk_id).order_by(KioskLocation.start_date.desc()).all()
    
    return render_template('location/kiosk_history.html', 
                         kiosk=kiosk, 
                         locations=locations, 
                         history=history)

@bp.route('/api/add', methods=['POST'])
def add_location():
    """API para agregar una nueva ubicación"""
    data = request.get_json()
    
    try:
        location = Location(
            name=data['name'],
            description=data.get('description'),
            address=data['address'],
            latitude=data['latitude'],
            longitude=data['longitude']
        )
        db.session.add(location)
        db.session.commit()
        
        return jsonify({'message': 'Ubicación creada exitosamente', 'location': location.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error al crear la ubicación: {str(e)}'}), 400

@bp.route('/api/update/<int:location_id>', methods=['PUT'])
def update_location(location_id):
    """API para actualizar una ubicación"""
    location = Location.get_location_by_id(location_id)
    data = request.get_json()
    
    try:
        location.update(data)
        return jsonify({'message': 'Ubicación actualizada exitosamente', 'location': location.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error al actualizar la ubicación: {str(e)}'}), 400

@bp.route('/api/delete/<int:location_id>', methods=['DELETE'])
def delete_location(location_id):
    """API para eliminar una ubicación"""
    location = Location.get_location_by_id(location_id)
    
    try:
        location.delete()
        return jsonify({'message': 'Ubicación eliminada exitosamente'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error al eliminar la ubicación: {str(e)}'}), 400

@bp.route('/api/kiosks/<int:location_id>')
def get_location_kiosks(location_id):
    """API para obtener los kiosks de una ubicación"""
    location = Location.get_location_by_id(location_id)
    kiosks = [kiosk.to_dict() for kiosk in location.kiosks]
    return jsonify(kiosks)

@bp.route('/api/assign-kiosk', methods=['POST'])
def assign_kiosk():
    """API para asignar una ubicación a un kiosk"""
    data = request.get_json()
    
    if not data or 'kiosk_id' not in data or 'location_id' not in data:
        abort(400, description="Se requieren kiosk_id y location_id")
    
    kiosk = Kiosk.query.get_or_404(data['kiosk_id'])
    location = Location.query.get_or_404(data['location_id'])
    
    # Si hay una ubicación actual, cerrar su período
    current_location = KioskLocation.query.filter_by(
        kiosk_id=kiosk.id, 
        end_date=None
    ).first()
    
    if current_location:
        current_location.end_date = datetime.utcnow()
    
    # Crear nuevo registro de ubicación
    new_location = KioskLocation(
        kiosk_id=kiosk.id,
        location_id=location.id,
        notes=data.get('notes', '')
    )
    
    try:
        db.session.add(new_location)
        db.session.commit()
        return jsonify({'message': 'Ubicación asignada exitosamente'})
    except Exception as e:
        db.session.rollback()
        abort(500, description=str(e)) 