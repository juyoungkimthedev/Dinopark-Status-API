# Dinopark Status API
REST API to expose Dinopark dinosaur status. The project runs on a docker container
and it is important to have Docker and Docker-Compose installed on your machine to run the app.

---------
## How to setup and run the app

- 

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

-------

### Data Access Layer choice - MongoDB (NoSQL)

Run MongoDB docker container from official MongoDB image.
This is for a test purpose.

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


------

### Code style checker and static analysis

Code style and static analysis can be done using `pycodestyle` and `pylint`
In the project root, run `./pycodestyle` and `./pylint`. This will run `pycodestyle`
and `pylint` binary files and return scores.


------

### Running test

- I have used `docker-compose` as a remote interpreter in PyCharm IDE, this means 
you can run, debug and test the app in an isolated environment right from the IDE.
useful link: https://www.jetbrains.com/help/ruby/using-docker-compose-as-a-remote-interpreter.html

Just in case you can't run test on your own machine, here are screenshots of successful tests:
