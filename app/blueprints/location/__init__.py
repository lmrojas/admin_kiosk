from flask import Blueprint

bp = Blueprint('location', __name__, 
               url_prefix='/location',
               template_folder='../../templates')

from app.blueprints.location import routes  # Importar rutas al final para evitar imports circulares 