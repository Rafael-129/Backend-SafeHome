#!/bin/bash
set -e

echo "Starting SafeHome Backend..."
cd /home/site/wwwroot

# Verificar si estamos en la estructura correcta
if [ ! -f "service/manage.py" ]; then
    echo "ERROR: manage.py not found. Trying Backend/service..."
    if [ ! -f "Backend/service/manage.py" ]; then
        echo "ERROR: manage.py not found in either location!"
        ls -la
        exit 1
    fi
    cd Backend/service
fi

# Ejecutar migraciones
echo "Running migrations..."
python manage.py migrate

# Iniciar Gunicorn
echo "Starting Gunicorn..."
exec gunicorn service.wsgi:application --bind 0.0.0.0:8000 --workers 4
