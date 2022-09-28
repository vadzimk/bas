# Blanket application strategy

## Overview
See **[Github page](https://github.com/vadzimk/bas)** 


## Usage
Create these two files (postgres-init-db.sh _and_ docker-compose.yml) and run commands in bash:  
```bash
chmod +x postgres-init-db.sh
docker-compose -f docker-compose.yml up
```
Application will be available on `localhost:80`  

#### postgres-init-db.sh
```sh
#!/bin/sh
set -e
psql -U $POSTGRES_USER -tc "SELECT 1 FROM pg_database WHERE datname = $DATABASE_NAME" \
| grep -q 1 || psql -U $POSTGRES_USER -c "CREATE DATABASE $DATABASE_NAME"
```


#### docker-compose.yml
```yaml
version: "3.5"

volumes:
  redis_data:
  postgres_data_prod:

networks:
  bas_prod_network:
    name: bas_prod_network

services:
  redis:
    image: redis
    container_name: redis_prod
    expose:
      - 6379
    command: [ 'redis-server', '--appendonly', 'yes' ]
    volumes:
      - redis_data:/data
    networks:
      - bas_prod_network

  postgres:
    image: postgres
    restart: unless-stopped
    container_name: postgres_prod
    expose:
      - 5432
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=1
      - DATABASE_NAME=bas
    volumes:
      - ./postgres-init-db.sh:/docker-entrypoint-initdb.d/postgres-init-db.sh
      - postgres_data_prod/:/var/lib/postgresql/data
    networks:
      - bas_prod_network

  adminer:
    image: adminer
    container_name: adminer_prod
    restart: unless-stopped
    ports:
      - "8080:8080"
    networks:
      - bas_prod_network

  flask_backend:
    container_name: bas_backend
    image: vadzimk/bas
    environment:
      - DATABASE_URL=postgresql://postgres:1@postgres_prod:5432/bas
      - CELERY_BROKER_URL=redis://redis_prod:6379/0
      - CELERY_RESULT_BACKEND=redis://redis_prod:6379/0
    ports:
      - "80:5000"
    networks:
      - bas_prod_network
    depends_on:
      - postgres
      - redis
```
