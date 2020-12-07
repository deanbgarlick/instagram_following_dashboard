docker-compose up -d --build
docker-compose exec flask flask db upgrade
docker-compose exec flask python manage.py create_db
docker-compose exec flask python manage.py seed_db
docker-compose exec flask uwsgi --py-autoreload 1 app.ini
