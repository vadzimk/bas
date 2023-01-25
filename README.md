# Blanket application strategy

## Overview

This app automates a headless browser to search for jobs on Indeed/Linkedin/Builtin job boards and presents results in a tabular form such that you can see all info about companies and job posts at a glance.  
It runs **in Docker locally** only and all data are saved to your database locally.   
You can 
 - create crawling tasks for Indeed, Linkedin, Builtin job boards  
 - view and remove unfit job posts from results view    
 - save notes about job posts and companies  
 - mute certain companies and remove all their posts from view
 - view and unmute muted companies
 - save job posts for later by marking them as 'plan apply' or 'applied'  


## Demo

![Current version demo search](Screenshot%202022-09-29%20app.png)
![Current version demo results](Screenshot%202022-09-29%20res.png)
![Current version demo plan-apply](Screenshot%202022-09-29%20plana.png)
![Current version demo company-filter](Screenshot%202022-09-29%20visibility.png)

## Stack

- React
- Tabulator
- Python
- Asyncio
- BeautifulSoup
- Playwright
- Flask
- SQLAlchemy
- Postgres
- Celery
- Redis
- GitLab CI
- Docker

## Usage

See [Docker Hub](https://hub.docker.com/r/vadzimk/bas) for usage


## If mock linkedin account 'expires'
- There is a button [UPDATE USER] to update Linkedin credentials once the previous account "expires".

## Development

<details>
<summary> create the file  "/.env.dev.postgres" </summary>
<pre>
POSTGRES_USER=postgres
POSTGRES_PASSWORD=1
DATABASE_NAME=bas
</pre>
</details>

```bash
# create and activate venv and install dependencies:
cd backend
pip insttall poetry==1.1.14
python -m venv .venv
. .venv/bin/activate
poetry install
playwright install chromium
playwright install-deps

# start dbms:
docker-compose -f docker-compose.dev.yml up -d

# create backend db migration:
cd backend/src  
flask db init  # adds support for db migrations  
flask db migrate # creates migration script  
flask db upgrade # applies changes to db  

# start celery worker:
celery -A app.celery worker --loglevel=info  --concurrency=1  # process 1 concurrent task in a queue

# start backend:
export FLASK_DEBUG=1
flask run -p 5000

# start frontend:
export PORT=3001
npm run start

# a separate script for manual testing of selectors, not part of the application
python -m bas_app.scraper.man   
``` 




## Diagrams
### Use-case
![Use case diagram](diagrams/Diagram-USE-CASE.png)
### Entity-relationship
![ER diagram](Screenshot%202022-09-29%20er.png)
