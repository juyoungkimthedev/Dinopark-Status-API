# Dinopark Status API
REST API to expose Dinopark dinosaur status. The project runs on a docker container
and it is important to have Docker and Docker-Compose installed on your machine to run the app.

Docker installation: https://docs.docker.com/get-docker/
Docker compose installation: https://docs.docker.com/compose/install/


### Useful Docker commands:

#### docker command: 

- `docker build -f ./Dockerfile .`
- `docker run -d -p 8080:80 dinoparkapi`
- `curl http://localhost:80`
- `docker rm -f <container_id>` 


#### docker-compose command:

Build publishable docker image by running:
- `docker-compose -f docker-compose.yml build`

Run the container with:
- `docker-compose -f docker-compose.yml up`

Run the container by detaching:
- `docker-compose -f docker-compose.yml up -d`

Exec into docker container:
- `docker exec -it <docker_container_id> bash`

Stop existing running docker container:
- `docker rm -f <docker_container_id>`


### Data Access Layer choice - MongoDB (NoSQL)

Run MongoDB docker container from official MongoDB image.
This is for a test purpose.