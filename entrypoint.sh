#!/bin/sh
python manage.py makemigrations
python manage.py migrate --noinput
python manage.py update_index
python manage.py runserver 0.0.0.0:80 --settings=iati.settings.dev
exec "$@"
