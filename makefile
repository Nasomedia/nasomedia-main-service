.PHONY: build, run, down, restart, db

build:
	sudo docker comopse build
up:
	sudo docker compose up -d --build

down:
	sudo docker compose down

restart:
	sudo docker compose restart

db:
	docker run --name postgres-container -d --restart unless-stopped \
  -p 5432:5432 -e POSTGRES_PASSWORD=postgres \
  -v postgres-data:/var/lib/postgresql/data postgres:latest