.PHONY: start-app
start-app:
	alembic upgrade head
	python asgi.py

.PHONY: test-app
test-app:
	pytest -s -v tests
