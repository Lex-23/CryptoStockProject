python manage.py migrate
python manage.py createsuperuser --no-input
python manage.py collectstatic --no-input
gunicorn cryptostock.wsgi:application --bind 0.0.0.0:${APP_PORT} --log-level info --timeout 180 --workers 3
