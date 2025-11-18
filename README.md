# SafeHome Backend API

Backend desarrollado con Django REST Framework para el sistema SafeHome.

## Requisitos

- Python 3.10+
- Django 5.2.8
- Django REST Framework 3.16.1

## Instalación

1. Crear y activar el entorno virtual:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Aplicar migraciones:
```bash
python manage.py migrate
```

4. Crear superusuario (opcional):
```bash
python manage.py createsuperuser
```

5. Ejecutar el servidor de desarrollo:
```bash
python manage.py runserver
```

## Endpoints

- `/admin/` - Panel de administración de Django
- `/api/` - Raíz de la API REST
- `/api/health/` - Health check del servidor

## Configuración

El proyecto está configurado con:
- **Django REST Framework** para la creación de APIs RESTful
- **Django CORS Headers** para permitir peticiones desde el frontend (puertos 5173 y 3000)
- **SQLite** como base de datos por defecto

### CORS

Los orígenes permitidos están configurados en `settings.py`:
- `http://localhost:5173` (Vite dev server)
- `http://localhost:3000` (React/Next.js dev server)

## Estructura del Proyecto

```
service/
├── api/                # Aplicación principal de la API
│   ├── views.py       # Vistas y ViewSets de la API
│   ├── serializers.py # Serializadores de datos
│   ├── urls.py        # URLs de la API
│   └── models.py      # Modelos de datos
├── service/           # Configuración del proyecto
│   ├── settings.py    # Configuración principal
│   ├── urls.py        # URLs principales
│   └── wsgi.py        # Configuración WSGI
├── manage.py          # Script de gestión de Django
└── requirements.txt   # Dependencias del proyecto
```

## Desarrollo

Para crear nuevos modelos, serializers y views, trabajar en la aplicación `api/`.

### Ejemplo de uso:

```python
# En api/models.py - definir modelos
# En api/serializers.py - crear serializers
# En api/views.py - crear views/viewsets
# En api/urls.py - registrar URLs
```
