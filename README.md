# Sistema de Administración de Kiosks
Versión: 3.1.0

## Descripción
Sistema de administración para kiosks que utiliza:
- Arquitectura MVT (Model-View-Template)
- WebSockets para comunicación en tiempo real
- Sistema de logs detallado
- UI responsiva con tarjetas de estado
- Cumplimiento con estándares GLI e ISO

## Características Principales
- **Monitoreo en Tiempo Real**:
  - CPU, RAM, Disco
  - Temperatura y Humedad
  - Estado de Red y UPS
  - Impresora y Periféricos

- **Sistema de Alertas**:
  - Umbrales configurables
  - Notificaciones en tiempo real
  - Logs detallados
  - Auditoría completa

- **Interfaz de Usuario**:
  - Tarjetas de estado en tiempo real
  - Dashboard con métricas
  - Visualización de logs
  - Mapas de ubicación

- **Seguridad**:
  - Autenticación WebSocket
  - Rate limiting
  - Auditoría de acciones
  - Logs inmutables

## Tecnologías
- **Backend**:
  - Flask 3.0.0
  - PostgreSQL
  - WebSockets
  - Flask-SQLAlchemy
  - Flask-Migrate
  
- **Frontend**:
  - Bootstrap
  - jQuery
  - WebSocket client
  - Charts.js

## Requisitos
- Python 3.8+
- PostgreSQL 12+
- Ambiente virtual Python
- Node.js (para algunas dependencias frontend)

## Instalación Rápida

1. Clonar repositorio:
```bash
git clone https://github.com/lmrojas/admin_kiosk.git
cd admin_kiosk
```

2. Crear ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno (.env):
```
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:pass@localhost/admin_kiosk
MAIL_USERNAME=lm_test@quattropy.net
MAIL_PASSWORD=a123a_*.*
```

5. Inicializar base de datos:
```bash
flask db init
flask db migrate
flask db upgrade
```

## Estructura del Proyecto
```
admin_kiosk/
├── app/
│   ├── models/            # Modelos (M)
│   ├── views/            # Vistas (V)
│   ├── templates/        # Templates (T)
│   ├── static/          # Archivos estáticos
│   ├── websocket/       # Manejo de WebSocket
│   ├── ai/             # Integración de IA
│   └── __init__.py     # create_app y config
├── migrations/         # Migraciones BD
├── scripts/           # Scripts auxiliares
├── tests/            # Tests unitarios
├── requirements.txt  # Dependencias
└── config.py        # Configuración
```

## Documentación
- [Documentación Completa](docs/documentacion_completa_sistema_kiosk.txt)
- [Mejoras del Sistema](docs/mejoras_sistema_kiosk.txt)

## Contribuir
1. Fork el repositorio
2. Crear rama para feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## Autor
lmrojas (lmrojasramirez@gmail.com)

## Licencia
Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE.md](LICENSE.md) para detalles 