setup: build render up

build-quarto: docker-compose.yml Dockerfile .env
	cp .env automated_reports/env_file
	docker compose build quarto

build-automated-reports: docker-compose.yml website/Dockerfile .env
	docker compose build automated_reports

build: build-quarto build-automated-reports

render: automated_reports/*.qmd
	docker compose run quarto quarto render automated_reports

up:
	docker compose up -d

down:
	docker compose down

clean:
	docker compose down --rmi all -v

