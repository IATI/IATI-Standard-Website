#!/bin/bash
set -e

if [[ -z "${DATABASE_URL}" ]]; then
  until PGPASSWORD=$DATABASE_PASS psql -h $DATABASE_HOST -p $DATABASE_PORT -d $DATABASE_NAME -U $DATABASE_USER -c '\l'; do
    >&2 echo "Azure postgres is unavailable - sleeping"
    sleep 1
  done
else
  until psql $DATABASE_URL -c '\l'; do
    >&2 echo "Postgres is unavailable - sleeping"
    sleep 1
  done
fi


python manage.py collectstatic --noinput
python manage.py migrate --noinput
python manage.py compilemessages

rc-service elasticsearch.service start
rc-service celeryd start
rc-service rabbitmq-server.service start

exec "$@"
