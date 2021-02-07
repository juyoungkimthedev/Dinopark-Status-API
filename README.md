# Dinopark Status API

REST API to expose Dinopark status. Dinopark Status API exposes endpoints
for maintenance and safety status for a given unique zone identifier. 

The project runs on a docker container and it is important to have 
**Docker** and **Docker-Compose** installed on your machine to run the app.

-----

## API Specification

I have created a `swagger contract` for Dinopark Status API. It is commonly known as OpenAPI specification.
The API contract is written in `YAML` file. You can find the contract from `dinopark_status_api/templates/swagger.yaml`.

Please view the *prettier* version of the contract from online swagger editor: `https://editor.swagger.io/`.
Simply copy content of `swagger.yaml` and paste it onto the online editor.

Example:

![Screenshot](example_screenshots/swagger.png)


-----


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


Example test result screenshots:

**Maintenance required:**

![Screenshot](example_screenshots/maintenance_required.png)

**Maintenance not required**

![Screenshot](example_screenshots/maintenance_not_required.png)

**Zone not in NUDLS logs**
![Screenshot](example_screenshots/maintenance_status_bad_request_no_zone.png)


-------

### Data Access Layer choice - MongoDB (NoSQL)

In this project I'm running MongoDB docker container from official MongoDB image.
This is for a test purpose. See: https://hub.docker.com/_/mongo

useful MongoDB commands:

To see data entries inside MongoDB instance created from docker
- `docker exec -it <mongo_db_instance_name> bash`

To see database and collection inside the mongo container shell
- `mongo` - start mongo shell inside mongodb container
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

**test_api_error_handler.py**

![Screenshot](example_screenshots/test_api_definition_1.png)


------

### How I approached the problem

I first looked at the requirements outlined from introduction page and I went on reading the given information
and try to understand the bigger picture. I thought about what problems this API need to solve (provide information
about zones in the park to reduce mortality rate) and tried to 
gather as much information as possible i.e. maintenance is needed for every 30 days etc.

In terms of maintenance, I retrieved maintenance information from NUDLS logs and worked out
the difference between today's date (when API was called) and the last date the maintenance was performed.
If the difference in days is <= 30, means no maintenance is required. If difference is > 30, maintenance is required.

After seeing the bigger picture and understanding the problem, I went on designing the endpoints and general architecture
of the API system. I created an API contract using swagger file that outlines all the endpoints and how to use the API.
Also thought about which database system I want to use for the API.

I went on creating basic codebase for the API in Python Flask micro-framework and started building a
minimum viable product (MVP) as quickly as possible. After making an MVP, I integrated MongoDB (choice of my DB)
using docker and created basic database integration. After that, I wrote basic tests.

After writing basic test, I incorporated required business logic in the API endpoints and finished tests with `mocking`
included where necessary. Here `mocking` I'm referring to mocking HTTP request and response. The test also runs integration test 
with MongoDB instance created locally.

End to end test for all endpoints done after development.

------

### Things to do differently?

- I would create MongoDataAccessLayer class interface with methods. Didn't want to make the project too complex.
Creating a Mongo DAL class interface would make mocking and testing a lot eaiser.

- Use production ready WSGI HTTP server such as Gunicorn.
Currently the project uses Flask's default web server which is not suitable for production level.

- Database choice. I would use a cloud provider hosted DB. Such as Azure Cosmos DB.

- Perhaps, add OAuth authorization protocol using JWT as a token

- Maybe use `FastAPI` framework which reduces development time.

- In terms of business logic, I would engage a lot more with the stakeholders
to find out if there are any edge cases to write more robust tests. For example, will
NUDLS monitoring log return multiple logs with same zones? This enables a developer
to design more robust system.


------

### What I learned during the project 

- I learned that understanding the problem before coding is really, really important.
- I learned communication with backend consumers is really important to understand the requirements.
- I learned writing readable, production level code is really important for maintenance later.
- I learned writing good and robust tests that covers edge cases is crucial.
- More technically, I learned how to setup MongoDB instance locally and spin up using docker-compose to integrate with the API.
- I learned to write detailed `README.md` which is really important for someone who doesn't have context about the project.  

------

### How I think the challenge can be improved?

I think the assignment has good components to assess a developer's skills so I don't think it has to be more fancier. 
But perhaps, you can include a task that involves more HTTP methods such as DELETE/PUT etc. Or you can ask the candidate
to implement a OAuth protocol but maybe that will take a bit longer to complete. Or perhaps, you can give the candidate
a free tier cloud resource and ask the candidate to host the app in cloud or use cloud hosted DB to see the data real time. 

------

### Technical questions outlined:

A.


B. 


C.