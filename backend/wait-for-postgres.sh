#!/bin/sh
# wait-for-postgres.sh

set -e

CONNECTION_STRING="$1"
shift

until pg_isready -d "$CONNECTION_STRING"; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command"
exec "$@"

