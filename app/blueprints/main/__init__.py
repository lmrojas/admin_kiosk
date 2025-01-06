from flask import Blueprint

bp = Blueprint('main', __name__,
               template_folder='../../templates')  # Usar plantillas globales

from app.blueprints.main import routes  # Importar rutas al final para evitar imports circulares 