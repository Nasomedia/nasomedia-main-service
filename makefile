.PHONY: build, run, down, restart, db, deploy

build:
	sudo docker-comopse build
up:
	sudo docker-compose up -d --build

down:
	sudo docker-compose down --volumes

restart:
	sudo docker-compose restart

deploy:
	sudo docker stack deploy -c docker-compose.yml main-service
	
db:
	docker run --name postgres-container -d --restart unless-stopped \
  -p 5432:5432 -e POSTGRES_PASSWORD=postgres \
  -v postgres-data:/var/lib/postgresql/data postgres:latest