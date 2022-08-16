#!/bin/bash
set -e
. /venv/bin/activate
cd /app/src
if [ ! -d /app/src/migrations ];
then
  flask db init; # adds support to db migrations
  flask db migrate; # creates migration script
fi;
flask db upgrade # applies changes to db
exec gunicorn --bind 0.0.0.0:5000 app:app