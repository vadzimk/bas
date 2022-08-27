#!/bin/sh
set -e
psql -U $POSTGRES_USER -tc "SELECT 1 FROM pg_database WHERE datname = $DATABASE_NAME" | grep -q 1 || psql -U $POSTGRES_USER -c "CREATE DATABASE $DATABASE_NAME"