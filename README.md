# Dinopark Status API

REST API to expose Dinopark status. Dinopark Status API exposes endpoints
for maintenance and safety status for a given unique zone identifier. 

The project runs on a docker container and it is important to have 
**Docker** and **Docker-Compose** installed on your machine to run the app.

----

## How to setup, run and test the app

The app runs on docker container with docker-compose. 
If you don't have docker installed, please follow the guide below:

- Docker installation: https://docs.docker.com/get-docker/
- Docker compose installation: https://docs.docker.com/compose/install/

Also install Python 3 if you don't have Python installed on your machine.

-----

### Useful Docker commands:

#### docker command for Dockerfile: 

Build docker image from the Dockerfile
- `docker build -f ./Dockerfile .`

Run docker container with ports
- `docker run -d -p 5001:80 dinoparkapi`

Hit the endpoint
- `curl http://localhost:5001/<path>...`

How to remove running docker container gracefully
- `docker rm -f <container_id>` 


#### docker-compose command:

Build publishable docker image by running:
- `docker-compose -f docker-compose.yml build`

Run the container with:
- `docker-compose -f docker-compose.yml up`

Run the container by detaching. By doing this you can exec into container:
- `docker-compose -f docker-compose.yml up -d`

Exec into docker container:
- `docker exec -it <docker_container_id> bash`

Stop existing running docker container:
- `docker rm -f <docker_container_id>`

-------

### Running the app and testing

A. In the root project directory, build docker image. This might take some time depending on your system,
as you have to download base Python and MongoDB images and install dependencies for the first time.

Run in the project root directory - `docker-compose -f docker-compose.yml build`

B. Spin up App and MongoDB docker containers from the built images. 

Run - `docker-compose -f docker-compose.yml up`

You can run in detach mode to be able to exec into containers if you want with the below command:

`docker-compose -f docker-compose.yml up -d`

C. When docker containers spin up locally using docker-compose.yml, now you can test the app.
This will spin up the API and MongoDB instance.
First hit health endpoint to see if the app is running fine:

To test health endpoint:
- `localhost:5001/dinopark_status/v1/`

To test zone maintenance status:
- `localhost:5001/dinopark_status/v1/maintenance_status?zone=A1`

To test zone safety status:
- `localhost:5001/dinopark_status/v1/safety_status?zone=A1`


Example test result:


-------

### Data Access Layer choice - MongoDB (NoSQL)

In this project I'm running MongoDB docker container from official MongoDB image.
This is for a test purpose. See: https://hub.docker.com/_/mongo

useful MongoDB commands:

To see data entries inside MongoDB instance created from docker
- `docker exec -it <mongo_db_instance_name> bash`

To see database and collection inside the mongo container shell
- `mongo`
- `show dbs`
- `use <database_name>`
- `show collections`
- `use <collection_name>`
- `db.stats`
- `db.<collection_name>.find().pretty()` - show all the entries
- `db.<collection_name>.remove({})` - to delete all documents

MongoDB (document DB) is a good choice for unstructured data and we can set
the zone number as a partition key to improve the query performance when searching for
status of a zone.


------

### Code style checker and static analysis

Code style and static analysis can be done using `pycodestyle` and `pylint`
In the project root, run `./pycodestyle` and `./pylint`. This will run `pycodestyle`
and `pylint` binary files and return scores.


------

### Running code test

- I have used `docker-compose` as a remote interpreter in PyCharm IDE, this means 
you can run, debug and test the app in an isolated environment right from the IDE.
useful link: https://www.jetbrains.com/help/ruby/using-docker-compose-as-a-remote-interpreter.html

Just in case you can't run test on your own machine, the screenshots are included below:


------

### How I approached the problem


------

### Things to do differently?

- Use production ready WSGI HTTP server such as Gunicorn.
Currently the project uses Flask's default web server which is not suitable for production level.

- Database choice. Cloud hosted DB.

- I would create MongoDataAccessLayer class interface with methods. Didn't want to make the project too complex.
Creating a Mongo DAL class interface would make mocking and testing a lot eaiser.

- Add OAuth authorization protocol using JWT as a token

------

### What I learned during the project 

------

### How I think you can improve the challenge

------

### Technical questions outlined: