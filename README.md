# Blanket application strategy

(Job board scrapper)

## Overview

This is an Indeed/Linkedin job board scrapper.  
It runs in Docker locally only.
It will scape Linkedin (and in soon Indeed) job boards for you and let you select eligible companies and listings.  
You can additionaly use auto-apply browser extensions:
[joinrhubarb](www.joinrhubarb.com),
[easyjobs](www.easyjobs.so),
[simplify](www.simplify.jobs)
to save even more time on your applications


## Demo

![Current version demo search](Screenshot%202022-08-26%20at%2012.12.04%20PM.png)
![Current version demo results](Screenshot%202022-08-26%20at%2012.16.28%20PM.png)

## Stack

- Vanilla JS ~> React
- Tabulator
- Python
- Asyncio
- BeautifulSoup
- Playwright
- Flask
- SQLAlchemy
- Sqlite
- Celery
- Redis

## Usage

```bash
chmod +x postgres-init-db.sh
docker-compose -f docker-compose.yml up
```
Application will be available on localhost:80  


## Limitations of the current version
- Generally Linkedin blocks you if you browse too much. There is a delay on crawling, but it is not adjusted to prevent blocking. There is a button to update Linkedin credentials once the previous account gets blocked.
- Current version only has Linkedin Tasks in the frontend.  Indeed tasks feature frontend is not implemented.  
- Playwright by Microsoft has a bug that leaks memory. I did not know that, so the headless browser may crash with error [Navigation failed because page crashed!](https://github.com/microsoft/playwright/issues/6319)

## Development
```bash
docker-compose -f docker-compose.dev.yml up -d
cd src  
flask db init  _# adds support to db migrations_  
flask db migrate _# creates migration script_  
flask db upgrade _# applies changes to db_  
celery -A app.celery worker --loglevel=info  --concurrency=1
export FLASK_DEBUG=1
flask run -p 5000
``` 



## Diagrams
### Use-case
![Use case diagram](diagrams/Diagram-USE-CASE.png)
### Entity-relationship
![ER diagram](Screenshot%202022-08-21%20at%206.48.44%20PM.png)

