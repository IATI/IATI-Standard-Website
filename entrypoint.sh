#!/bin/bash
set -e

>&2 echo "$DATABASE_URL"
until psql $DATABASE_URL -c '\l'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done


python manage.py collectstatic --noinput
python manage.py migrate --noinput
python manage.py compilemessages

rc-service elasticsearch.service start
rc-service celeryd start
rc-service rabbitmq-server.service start

exec "$@"