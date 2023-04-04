
celery.dev:
	cd backend/src && celery -A app.celery worker --loglevel=info  --concurrency=1

run.celery.flower:
	cd backend/src && celery -A app.celery flower --port=5556

backend.dev:
	cd backend/src && export FLASK_DEBUG=1 && flask run -p 5000

frontend.dev:
	cd frontend && export PORT=3001 && npm run start

migrate:
	cd backend && flask db migrate -m "$1"

upgrade:
	cd backend && flask db upgrade

redis.clear:
	docker exec redis_dev redis-cli -c "flushall"
