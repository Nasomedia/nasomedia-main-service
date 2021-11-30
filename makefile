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
