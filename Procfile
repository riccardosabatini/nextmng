web: gunicorn -b 0.0.0.0:$PORT -w 1 -k sync --worker-connections=10 -c gunicorn_conf_heroku.py nextmng.wsgi:application
celeryd: python manage.py celery worker -A nextmng -E --maxtasksperchild=1000 -c 3 
