web: gunicorn -b 0.0.0.0:$PORT -w 1 -k sync --worker-connections=10 -c gunicorn_conf_heroku.py nextmng.wsgi:application
celeryd: celery -A nextmng worker --loglevel=info -E