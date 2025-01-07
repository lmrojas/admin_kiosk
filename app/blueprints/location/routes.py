from flask import render_template, jsonify, request, current_app, flash, redirect, url_for
from app.blueprints.location import bp
from app.models.location import Location
from app.extensions import db
from datetime import datetime
from sqlalchemy import func

@bp.route('/')
def index():
    """Vista principal de locations"""
    current_app.logger.info('Accediendo a la vista de locations')
    locations = Location.query.all()
    
    # Calcular estadísticas
    total_kiosks = sum(len(location.kiosks) for location in locations)
    avg_kiosks_per_location = total_kiosks / len(locations) if locations else 0
    
    return render_template('location/index.html', 
                         locations=locations,
                         total_kiosks=total_kiosks,
                         avg_kiosks_per_location=avg_kiosks_per_location)

@bp.route('/create', methods=['GET', 'POST'])
def create():
    """Vista para crear una nueva ubicación"""
    if request.method == 'POST':
        try:
            location = Location(
                name=request.form['name'],
                address=request.form['address'],
                latitude=float(request.form['latitude']),
                longitude=float(request.form['longitude']),
                description=request.form.get('description', '')
            )
            db.session.add(location)
            db.session.commit()
            flash('Ubicación creada exitosamente', 'success')
            return redirect(url_for('location.index'))
        except Exception as e:
            current_app.logger.error(f'Error al crear ubicación: {str(e)}')
            flash('Error al crear la ubicación', 'danger')
            db.session.rollback()
    
    return render_template('location/create.html')

@bp.route('/api/create', methods=['POST'])
def api_create():
    """API para crear una ubicación"""
    try:
        data = request.get_json()
        location = Location(
            name=data['name'],
            address=data['address'],
            latitude=float(data['latitude']),
            longitude=float(data['longitude']),
            description=data.get('description', '')
        )
        db.session.add(location)
        db.session.commit()
        return jsonify({'success': True, 'location': location.to_dict()})
    except Exception as e:
        current_app.logger.error(f'Error al crear ubicación: {str(e)}')
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

@bp.route('/api/update/<int:id>', methods=['PUT'])
def api_update(id):
    """API para actualizar una ubicación"""
    try:
        location = Location.query.get_or_404(id)
        data = request.get_json()
        
        location.name = data.get('name', location.name)
        location.address = data.get('address', location.address)
        location.latitude = float(data.get('latitude', location.latitude))
        location.longitude = float(data.get('longitude', location.longitude))
        location.description = data.get('description', location.description)
        
        db.session.commit()
        return jsonify({'success': True, 'location': location.to_dict()})
    except Exception as e:
        current_app.logger.error(f'Error al actualizar ubicación: {str(e)}')
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400 

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    """Vista para editar una ubicación existente"""
    location = Location.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            location.name = request.form['name']
            location.address = request.form['address']
            location.latitude = float(request.form['latitude'])
            location.longitude = float(request.form['longitude'])
            location.description = request.form.get('description', '')
            location.updated_at = datetime.utcnow()
            
            db.session.commit()
            flash('Ubicación actualizada exitosamente', 'success')
            return redirect(url_for('location.index'))
        except Exception as e:
            current_app.logger.error(f'Error al actualizar ubicación: {str(e)}')
            flash('Error al actualizar la ubicación', 'danger')
            db.session.rollback()
    
    return render_template('location/edit.html', location=location) 