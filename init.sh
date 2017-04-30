celery -A securedHome worker -l info
celery -A securedHome beat
python manage.py runserver
