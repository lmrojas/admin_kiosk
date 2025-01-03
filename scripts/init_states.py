from app import create_app, db
from app.models.state import State

def init_states():
    """Inicializar estados básicos en la base de datos"""
    app = create_app()
    with app.app_context():
        # Crear estados si no existen
        states = [
            {'id': 1, 'name': 'Normal', 'color': 'success'},
            {'id': 2, 'name': 'Warning', 'color': 'warning'},
            {'id': 3, 'name': 'Crítico', 'color': 'danger'}
        ]
        
        for state_data in states:
            state = State.query.get(state_data['id'])
            if not state:
                state = State(**state_data)
                db.session.add(state)
        
        db.session.commit()
        print("Estados inicializados correctamente")

if __name__ == '__main__':
    init_states() 