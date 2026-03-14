#!/bin/bash
cd /home/site/wwwroot
python manage.py migrate
gunicorn service.wsgi:application --bind=0.0.0.0 --workers 4
