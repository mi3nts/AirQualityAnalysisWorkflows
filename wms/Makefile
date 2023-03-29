setup: build up

build-nodered: nodered-docker/Dockerfile .env
	docker compose build nodered

build-wms: skinnywms/Dockerfile .env
	docker compose build wms

build-dashboards: build-nodered build-wms .env

build: build-dashboards

up:
	docker compose up -d

down:
	docker compose down

clean:
	docker compose down --rmi all -v
