python manage.py collectstatic && gunicorn --workers 2 main_app.wsgi
