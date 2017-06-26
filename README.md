# Address resolver API

## Libraries used 
* Django
* django rest framework (API)
* django-rest-swagger (documentation)
* postgis (spatial database) plugin for postgres database. Postgres db with postgis EXTENSION is required.

## Description

Vertion 1 of a RESTFul API address with geolocation. Converting addresses 
(like "1600 Amphitheatre Parkway, Mountain View, CA") into geographic 
coordinates, resolving then throw google maps geocoding and elevation api.

## End Points

### Address
* `POST /api/address/`
* `GET /api/address/`
* `GET /api/address/{pk}`

## Documentation
All the API docs are available in **http://0.0.0.0:8000/docs/** builded with **Django REST Swagger**

## Installation 
### Docker compose (easy way) though docker-compose is required

`docker-compose build`

`docker-compose up`

### By your self

### Install the system dependencies
* **git** 
* **pip**

### Get the code
* Clone the repository

`git clone https://gitlab.com/ifreddyrondon/address-resolver`

### Install the project dependencies

`pip install -r requirements/development.txt`

### Run the command to generate the database

`cd addressresolver`

`python manage.py migrate --settings=config.settings.dev`

### Run the server
Make sure set the env var DATABASE_URL.
e.g. DATABASE_URL=postgis://postgres:@db/postgres

`python manage.py runserver --settings=config.settings.dev` the application will be running on port 8000 **http://0.0.0.0:8000/**

# Test
## Run the test

`python manage.py test --settings=config.settings.dev`
