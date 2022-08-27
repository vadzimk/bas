#!/bin/bash
set -e
. wait-for-postgres.sh $DATABASE_URL
. /venv/bin/activate
cd /usr/src/app/src
if [ ! -d migrations ];
then
  flask db init; # adds support to db migrations
  flask db migrate; # creates migration script
fi;
flask db upgrade # applies changes to db
exec celery -A app.celery worker --loglevel=info --concurrency=1 &
exec gunicorn --bind 0.0.0.0:5000 --workers=1 app:app