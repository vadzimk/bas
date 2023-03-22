FROM apache/superset
WORKDIR /app
# Switching to root to install the required packages
USER root
# Example: installing the driver to connect to the metadata database
# if you prefer Postgres, you may want to use `psycopg2-binary` instead
RUN pip install psycopg2-binary

# Switching back to using the `superset` user

COPY superset-init.sh .
RUN chmod +x superset-init.sh

ENTRYPOINT ["/app/superset-init.sh"]