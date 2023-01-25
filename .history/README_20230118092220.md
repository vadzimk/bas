# Blanket application strategy

## Overview

This app automates headless browser to search for jobs on Indeed/Linkedin/Builtin job-boards and presents results in a tabular form such that you can see all info about companies and openings at a glance.  
It runs **in Docker locally** only and all data are saved to your database locally.   
You can 
 - create crawling tasks for Indeed, Linkedin, Builtin job boards  
 - remove unfit listings from results view    
 - save notes about listings and companies  
 - automatically mute certain companies  
 - mark listings as 'plan apply' or 'applied'  



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

## Usage

See [Docker Hub](https://hub.docker.com/r/vadzimk/bas) for usage


## If mock linkedin account 'expires'
- There is a button [UPDATE USER] to update Linkedin credentials once the previous account "expires".

## Development
```bash
docker-compose -f docker-compose.dev.yml up -d
cd src  
flask db init  # adds support for db migrations  
flask db migrate # creates migration script  
flask db upgrade # applies changes to db  
celery -A app.celery worker --loglevel=info  --concurrency=1  # process 1 concurrent task in a queue
export FLASK_DEBUG=1
flask run -p 5000
python -m bas_app.scraper.man # separate script for manual testing of selectors, not part of application  
``` 



## Diagrams
### Use-case
![Use case diagram](diagrams/Diagram-USE-CASE.png)
### Entity-relationship
![ER diagram](Screenshot%202022-09-29%20er.png)
