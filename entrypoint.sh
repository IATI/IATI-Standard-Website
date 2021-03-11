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

gunicorn iati.wsgi:application --bind 0.0.0.0:5000 --workers 3 --worker-connections 1000 --worker-class gevent --timeout 0 > gunicorn.log 2>&1 &

/usr/sbin/crond -f -l 8 &

python manage.py collectstatic --noinput
python manage.py migrate --noinput
python manage.py compilemessages

# rc-service elasticsearch.service start
# rc-service celeryd start
# rc-service rabbitmq-server.service start

exec "$@"
