IMAGE_NAME = "fastapi-cookiecutter"

build:
	docker build --build-arg ENVIRONMENT=DEV -t ${IMAGE_NAME}:latest .

log:
	docker logs -f app

up:
	docker-compose --env-file ./env/dev.env up -d
	make log

down:
	docker-compose --env-file ./env/dev.env down

test:
	docker-compose --env-file ./env/test.env up -d
	docker exec -it app pytest -v
	docker-compose --env-file ./env/test.env down

.PHONY: build log up down test
