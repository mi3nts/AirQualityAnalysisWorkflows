setup: build up

build-nodered: influxdb/nodered-docker/Dockerfile .env
	docker compose --env-file .env -f ./influxdb/docker-compose.yml build nodered

build-influxdb: influxdb/influxdb-docker/Dockerfile .env
	docker compose --env-file .env -f ./influxdb/docker-compose.yml build influxdb

build-grafana: influxdb/grafana-docker/Dockerfile .env
	docker compose --env-file .env -f ./influxdb/docker-compose.yml build grafana

build-dashboards: build-nodered build-influxdb build-grafana .env

build-quarto: quarto/docker-compose.yml quarto/Dockerfile .env
	cp .env quarto/automated_reports/env_file
	docker compose --env-file .env -f ./quarto/docker-compose.yml build quarto

build-automated-reports: quarto/docker-compose.yml quarto/website/Dockerfile .env
	docker compose --env-file .env -f ./quarto/docker-compose.yml build automated_reports

build-reports: build-quarto build-automated-reports


build: build-dashboards build-reports


# render: quarto/automated_reports/*.qmd
# 	docker compose -f ./quarto/docker-compose.yml run quarto quarto render automated_reports

up-dashboards:
	docker compose --env-file .env -f ./influxdb/docker-compose.yml up -d

up-reports:
	docker compose --env-file .env -f ./quarto/docker-compose.yml up -d

up: up-dashboards up-reports


clean-dashboards:
	docker compose --env-file .env -f ./influxdb/docker-compose.yml down --rmi all -v

clean-quarto:
	docker compose --env-file .env -f ./quarto/docker-compose.yml down --rmi all -v

clean: clean-dashboards clean-quarto
