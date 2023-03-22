#!/usr/bin/env sh
set -e

export SQLALCHEMY_DATABASE_URI="postgresql+psycopg2://${SUPERSET_POSTGRES_USER}:${SUPERSET_POSTGRES_PASSWORD}@${SUPERSET_POSTGRES_HOST}:${SUPERSET_POSTGRES_PORT}/${SUPERSET_POSTGRES_DATABASE}"
echo "SQLALCHEMY_DATABASE_URI=\"$SQLALCHEMY_DATABASE_URI\"" > /app/superset_config.py
export PYTHONPATH="${PYTHONPATH}:/app/superset_config.py"
export SUPERSET_CONFIG_PATH="/app/superset_config.py"

superset fab create-admin --username "$SUPERSET_ADMIN_USERNAME" --firstname Superset --lastname Admin --email "$SUPERSET_ADMIN_EMAIL" --password "$SUPERSET_ADMIN_PASSWORD"

# Initialize the database
superset db upgrade

# Create default roles and permissions
superset init

. /usr/bin/run-server.sh