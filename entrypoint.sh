#!/bin/bash
set -e

if [[ -z "${DATABASE_URL}" ]]; then
  until PGPASSWORD=$DATABASE_PASS psql -h $DATABASE_HOST -p $DATABASE_PORT -d $DATABASE_NAME -U $DATABASE_USER -c '\l'; do
    >&2 echo "Azure postgres is unavailable - sleeping"
    sleep 10
  done
else
  until psql $DATABASE_URL -c '\l'; do
    >&2 echo "Postgres is unavailable - sleeping"
    sleep 10
  done
fi

if [[ -z "${ELASTICSEARCH_URL}" ]]; then
  >&2 echo "Skipping Elasticsearch"
else
  >&2 echo "Starting Elasticsearch"
  rc-service elasticsearch.service start
fi

if [[ -z "${DEBUG_SERVER}" ]]; then
  gunicorn iati.wsgi:application --bind 0.0.0.0:5000 --workers $GUNICORN_WORKERS >> /var/log/gunicorn/gunicorn.log 2>&1 &
else
  >&2 echo "Debug flag detected, running local server instead of gunicorn"
  python3 manage.py runserver --settings iati.settings.dev 0.0.0.0:5000 >> /var/log/gunicorn/gunicorn.log 2>&1 &
fi


/usr/sbin/crond -f -l 8 &

python manage.py collectstatic --noinput
python manage.py migrate --noinput
python manage.py compilemessages
python manage.py update_index

exec "$@"
