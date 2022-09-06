# Blanket application strategy

(Job board crawler)

## Overview

This is an Indeed/Linkedin job board crawler.  
It runs in Docker locally only.  
All data are saved to database locally.  
Repeated postings are crawled only once.  
You can 
 - filter by postings to your liking  
 - mark deleted postings of no interest to you  
 - save notes about the postings and companies  
 - automatically ignore certain companies [not implemented]
 

You can additionaly use auto-apply browser extensions:
[joinrhubarb](www.joinrhubarb.com),
[easyjobs](www.easyjobs.so),
[simplify](www.simplify.jobs)
to save even more time on your applications


## Demo

![Current version demo search](Screenshot%202022-09-06%20app.png)
![Current version demo results](Screenshot%202022-09-06%20results.png)

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

See [Docker Hub](https://hub.docker.com/r/vadzimk/bas) for usage


## Limitations of the current version
- Generally Linkedin blocks you if you browse too much. There is a delay on crawling, but it is not adjusted to prevent blocking. There is a button [UPDATE USER] to update Linkedin credentials once the previous account gets blocked. 
- Playwright by Microsoft has a bug that leaks memory. I did not know that before selecting an automation framework, so the headless browser may crash with error [Navigation failed because page crashed!](https://github.com/microsoft/playwright/issues/6319)

## Development
```bash
docker-compose -f docker-compose.dev.yml up -d
cd src  
flask db init  # adds support to db migrations  
flask db migrate # creates migration script  
flask db upgrade # applies changes to db  
celery -A app.celery worker --loglevel=info  --concurrency=1  # process 1 concurrent task in a queue
export FLASK_DEBUG=1
flask run -p 5000
python -m bas_app.scraper.man # for manual testing of selectors  
``` 



## Diagrams
### Use-case
![Use case diagram](diagrams/Diagram-USE-CASE.png)
### Entity-relationship
![ER diagram](Screenshot%202022-09-06%20erd.png)

