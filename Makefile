DC = docker compose

.PHONY: app-start
app-start:
	alembic upgrade head
	python asgi.py

.PHONY: app-test
app-test:
	pytest -s -v tests

.PHONY: dc-start
dc-start:
	${DC} ud -d

.PHONY: dc-stop
dc-stop:
	${DC} down
