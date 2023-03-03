setup: build up update-buckets

build-nodered: nodered-docker/Dockerfile .env
	docker compose build nodered

build-influxdb: influxdb-docker/Dockerfile .env
	docker compose build influxdb

update-buckets: influxdb-docker/Dockerfile .env
	sleep 2
	docker compose exec influxdb bash /scripts/update_buckets.sh

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
