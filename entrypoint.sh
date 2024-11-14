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

until curl --output /dev/null --silent --head --fail ${ELASTICSEARCH_URL}; do
    >&2 echo "Elasticsearch is unavailable - sleeping"
    sleep 10
done

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
python manage.py createcachetable
python manage.py compress

exec "$@"
