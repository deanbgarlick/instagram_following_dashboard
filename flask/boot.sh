#!/bin/bash
sleep 20
flask db upgrade
python manage.py

# run the command to start uWSGI
uwsgi --py-autoreload 1 app.ini
