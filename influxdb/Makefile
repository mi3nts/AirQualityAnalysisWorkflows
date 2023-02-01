setup: build up

build-nodered: nodered-docker/Dockerfile .env
	docker compose build nodered

build-influxdb: influxdb-docker/Dockerfile .env
	docker compose build influxdb

build-grafana: grafana-docker/Dockerfile .env
	docker compose build grafana

build-dashboards: build-nodered build-influxdb build-grafana .env

build: build-dashboards

up:
	docker compose up -d

down:
	docker compose down

clean:
	docker compose down --rmi all -v
