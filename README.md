# Dinopark Status API
RESTful API to expose Dinopark dinosaur status

docker command: 

- `docker build -f ./Dockerfile .`
- `docker run -d -p 8080:80 dinoparkapi`
- `curl http://localhost:80`
- `docker rm -f <container_id>` 


docker-compose command:

Build publishable docker image by running:
- `docker-compose -f docker-compose.yml build`

Run the container with:
- `docker-compose -f docker-compose.yml up`

Run the container by detaching
- `docker-compose -f docker-compose.yml up -d`

Exec into docker container
- `docker exec -it <docker_container_id> bash`


* things to do:

1. add logic
2. create docker compose environment
3. create DB layer using sqllite
4. write test
5. readme complete.