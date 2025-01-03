from flask import Blueprint, render_template
from app.models import Kiosk, Location
from app.extensions import cache

bp = Blueprint('main', __name__)

@bp.route('/')
@cache.cached(timeout=60)
def index():
    """Vista principal del dashboard"""
    kiosks = Kiosk.query.all()
    locations = Location.query.all()
    
    # Calcular estadísticas
    total_kiosks = len(kiosks)
    total_locations = len(locations)
    online_kiosks = sum(1 for k in kiosks if k.status == 'online')
    
    return render_template('main/index.html',
                         kiosks=kiosks,
                         locations=locations,
                         total_kiosks=total_kiosks,
                         total_locations=total_locations,
                         online_kiosks=online_kiosks) 