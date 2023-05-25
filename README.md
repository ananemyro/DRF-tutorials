# Django REST Framework Tutorial Project
_Project ID: DRF_tutorials_
### Overview
The goal of this project was to build a Django web application using Django REST Framework. The project consists of two
apps, "_users_" and "_tutorials_", including multiple models that communicate with each other. The project logs are recorded
both locally and remotely, shipped to Elasticsearch by Filebeat and visualized through Kibana.

### Table of Contents
- [Architecture](#architecture)
- [Installation](#installation)
  * [Tooling](#tooling)
  * [Install with Docker](#install-with-docker)
- [API](#api)
  * [Authentication](#authentication)
  * [Swagger](#swagger)
- [Testing](#testing)
- [Logs](#logs)

### Architecture
The backend was built with [Django web framework](https://www.djangoproject.com/) interface with a
[MongoDB](https://www.mongodb.com/) database initially, but migrations to [PostgreSQL](https://www.postgresql.org/)
database were made later.
#### Apps
- "_users_":
  * defines permissions
  * handles user profile creation, modification, and removal
  * _types of views used_: ViewSets


- "_tutorials_":
  * defines "Skill", "Teacher", and "Tutorial" models
  * handles object creation, modification, and removal
  * _types of views used_: function-based, class-based (generics & mixins), ViewSets

### Installation
#### Tooling
[PyCharm](https://www.jetbrains.com/pycharm/) was the IDE used for the project. Additionally,
[DataGrip](https://www.jetbrains.com/datagrip/) was used to access the database.
#### Install with Docker
_Prerequisites_:
* [Docker](https://docs.docker.com/docker-for-mac/install/)
* [Git](https://git-scm.com/download/mac)

To install, open your terminal and clone the project in the desired directory:
```
git clone https://gitlab.int.bell.ca/an6115228/drf_tutorials.git
```
The requirements list can be found in DRFtutorials/requirements.txt.

### API
#### Authentication
To authenticate and make protected requests, a JWT token must be generated.
#### Swagger
To access Swagger documentation: http://127.0.0.1:8000/swagger/.

### Testing
To run all unit tests, run the following command in the terminal of the web container:
```
python3 manage.py test
```

### Logs
* To access logs locally, go to DRFtutorial/DRFtutorial/server.log.
* Alternatively, the logs can be viewed through Kibana: http://127.0.0.1:5601.
