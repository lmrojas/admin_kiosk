from flask import render_template, jsonify, request, current_app, flash, redirect, url_for
from app.blueprints.location import bp
from app.models.location import Location
from app.models.kiosk import Kiosk
from app.extensions import db

@bp.route('/')
def index():
    """Vista principal de locations"""
    current_app.logger.info('Accediendo a la vista de locations')
    
    try:
        # Obtener todas las ubicaciones
        locations = Location.query.all()
        
        # Calcular estadísticas
        total_locations = len(locations)
        total_kiosks = Kiosk.query.count()
        
        # Evitar división por cero
        avg_kiosks_per_location = round(total_kiosks / total_locations, 1) if total_locations > 0 else 0
        
        return render_template('location/index.html',
                            locations=locations,
                            total_kiosks=total_kiosks,
                            avg_kiosks_per_location=avg_kiosks_per_location)
    except Exception as e:
        current_app.logger.error(f'Error en vista de locations: {str(e)}')
        flash('Error al cargar las ubicaciones', 'error')
        return render_template('location/index.html',
                            locations=[],
                            total_kiosks=0,
                            avg_kiosks_per_location=0)

@bp.route('/api/list')
def api_list():
    """API para listar locations"""
    current_app.logger.info('Solicitando lista de locations vía API')
    locations = Location.query.all()
    return jsonify([l.to_dict() for l in locations])

@bp.route('/api/kiosks/<int:location_id>')
def get_location_kiosks(location_id):
    """API para obtener los kiosks de una ubicación"""
    current_app.logger.info(f'Solicitando kiosks de location {location_id}')
    location = Location.query.get_or_404(location_id)
    return jsonify({
        'kiosks': [
            {
                'id': k.id,
                'name': k.name,
                'serial_number': k.serial_number,
                'status': k.status,
                'last_connection': k.last_connection.isoformat() if k.last_connection else None
            } for k in location.kiosks
        ]
    })

@bp.route('/api/create', methods=['POST'])
def api_create():
    """API para crear una location"""
    current_app.logger.info('Creando nueva location')
    
    try:
        data = request.get_json()
        if not data:
            raise ValueError('No se recibieron datos')
            
        # Validar datos requeridos
        required_fields = ['name', 'address', 'latitude', 'longitude']
        for field in required_fields:
            if field not in data:
                raise ValueError(f'Falta el campo requerido: {field}')
        
        # Crear nueva ubicación
        location = Location(
            name=data['name'],
            address=data['address'],
            latitude=float(data['latitude']),
            longitude=float(data['longitude'])
        )
        
        db.session.add(location)
        db.session.commit()
        
        current_app.logger.info(f'Location {location.id} creada exitosamente')
        return jsonify({
            'status': 'success',
            'message': 'Ubicación creada exitosamente',
            'data': location.to_dict()
        })
        
    except ValueError as e:
        current_app.logger.error(f'Error de validación: {str(e)}')
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400
        
    except Exception as e:
        current_app.logger.error(f'Error creando location: {str(e)}')
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': 'Error interno al crear la ubicación'
        }), 500 