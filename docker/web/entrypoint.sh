#!/bin/sh
rm -rf /usr/src/app/public/static_root/
python3 /usr/src/app/manage.py collectstatic

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

exec "$@"