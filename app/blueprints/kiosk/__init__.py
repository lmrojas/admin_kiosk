from flask import Blueprint

bp = Blueprint('kiosks', __name__, 
               url_prefix='/kiosks',
               template_folder='../../templates')

from app.blueprints.kiosk import routes  # Importar rutas al final para evitar imports circulares 