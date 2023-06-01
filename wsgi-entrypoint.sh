#!/bin/sh

until cd /app/
do
    echo "Waiting fo server volume..."
done

until ./manage.py migrate

do  
    echo "Waiting fo db to be ready..."
    sleep 2
done

./manage.py collectstatic --noinput

gunicorn starnavi.wsgi --bind 0.0.0.0:8000 --workers 4 --threads 4

