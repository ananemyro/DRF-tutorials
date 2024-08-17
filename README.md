# Django REST Framework Tutorial Project

### Overview
This project demonstrates the development of a Django web application using Django REST Framework. It includes two primary apps, "_users_" and "_tutorials_", featuring multiple interrelated models. Logs are recorded both locally and remotely, with Filebeat shipping them to Elasticsearch for visualization in Kibana.

### Table of Contents
- [Architecture](#architecture)
- [Installation](#installation)
  * [Tooling](#tooling)
  * [Install with Docker](#install-with-docker)
- [API](#api)
  * [Authentication](#authentication)
  * [Swagger](#swagger)
  * [Making Requests](#making-requests)
- [Testing](#testing)
- [Logs](#logs)

### Architecture
The backend was built using the [Django web framework](https://www.djangoproject.com/), initially interfacing with a
[MongoDB](https://www.mongodb.com/) database. It was later migrated to [PostgreSQL](https://www.postgresql.org/).

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
The project was developed using [PyCharm](https://www.jetbrains.com/pycharm/) as the IDE and
[DataGrip](https://www.jetbrains.com/datagrip/) for database access.

#### Install with Docker
_Prerequisites_:
* [Docker](https://docs.docker.com/docker-for-mac/install/)
* [Git](https://git-scm.com/download/mac)

To install, open your terminal and clone the project into the desired directory:
```
git clone https://gitlab.int.bell.ca/an6115228/drf_tutorials.git
```
The requirements list can be found in 'DRFtutorials/requirements.txt'.

### API
#### Authentication
To authenticate and make protected requests, a JWT token must be generated.
#### Swagger
Access the Swagger documentation at: http://127.0.0.1:8000/swagger/.
#### Making Requests
Different behaviors are expected depending on the request type and authentication status. Examples include:
- Skill
  * permissions: IsAuthenticatedOrReadOnly
- Teacher
  * permissions: IsAuthenticated
  * if not authenticated, list of _names only_ can be viewed
- Tutorial
  * permissions: IsAuthenticated

### Testing
To run all unit tests, run the following command in the terminal of the web container:
```
python3 manage.py test
```

### Logs
* To access logs locally, navigate to 'DRFtutorial/DRFtutorial/server.log'.
* Logs can also be viewed through Kibana at: http://127.0.0.1:5601.
