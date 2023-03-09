# UOCIS322 - Project 6 #
Brevet time calculator with MongoDB, and a RESTful API!

Read about MongoEngine and Flask-RESTful before you start: [http://docs.mongoengine.org/](http://docs.mongoengine.org/), [https://flask-restful.readthedocs.io/en/latest/](https://flask-restful.readthedocs.io/en/latest/).



For this project, `Brevets` was organized into two separate services:

* Web (Front-end)
	* Time calculator (basically everything you had in project 4)
* API (Back-end)
	* A RESTful service to expose/store structured data in MongoDB.

## models.py:

This file defines two MongoEngine models, Checkpoint and Brevet.

The Checkpoint model is an embedded document that represents our list of brevet attributes in which we will store upon insertion and return upon fetch. . It has the following fields:

* `km`: A required float field representing the distance of the checkpoint in kilometers.
* `miles`: A required float field representing the distance of the checkpoint in miles.
* `location`: An optional string field representing the name of the checkpoint's location.
* `open`: A required string field representing the opening time of the checkpoint.
* `close`: A required string field representing the closing time of the checkpoint.

The Brevet model is our schema which contains the 3 common attributes of our brevet:

* `length`: A required float field representing the length of the brevet in kilometers.
* `start_time`: A required datetime field representing the start time of the brevet. 
* `checkpoints`: A required list field of Checkpoint embedded documents representing the checkpoints on the brevet route.

## brevet.py and brevets.py

This file defines a Flask-RESTful Resource called BrevetResource that interacts with the Brevet model.


BrevetResource provides the following endpoints:

`GET /brevet/<id>`: Retrieves a brevet with the given `id`.
`PUT /brevet/<id>`: Updates a brevet with the given `id`.
`DELETE /brevet/<id>`: Deletes a brevet with the given `id`.

BrevetsResource provides
`GET /brevets`: Gets data from where each and every brevet is stored.
`POST /brevets`: Saves our Brevet object and its correct fields.

When returning responses, the BrevetResource provides two options:

1. Return a Response object with the JSON payload, mimetype, and status code.

2. Return a Python dictionary with the JSON payload and status code.

Flask-RESTful's default behavior is to return a Python dictionary with the JSON payload and status code. 
However, since the Brevet model returns a MongoEngine query object instead of a dictionary, 
the `to_json()` method is used to convert the query result to a JSON string before returning it as a Response object.

## flask_api.py:

This file defines a Flask app and RESTful API that interacts with a MongoDB database.

The app connects to the MongoDB server specified in the MONGODB_HOSTNAME environment variable, and exposes our two resources: 
`BrevetResource` and `BrevetsResource`.

`BrevetResource` corresponds to a single brevet document in the database and supports the HTTP methods GET, PUT, 
and DELETE at the path /api/brevet/<id>, where <id> is the ID of the brevet.

`BrevetsResource` corresponds to all brevet documents in the database and supports the HTTP methods GET and POST at the path /api/brevets.

When the app is run, it starts a Flask server on the IP address `0.0.0.0` and the port specified in the PORT environment 
variable, or `5000` if PORT is not set. If the DEBUG environment variable is set, Flask will run in debug mode.

## flask_brevets.py:

In order to fully remove the database connection out of our initial flask app, we had to delete all of the logic in our mongodb python script.
From there, the previous mongodb methods `brevets_insert()` and `brevets_fetch()` were modified to respond to the api request using the `requests` library

### Curl Commands:


	* Using the schema, build a RESTful API with the resource `/brevets/`:
		* GET `http://API:PORT/api/brevets` should display all brevets stored in the database.
		* GET `http://API:PORT/api/brevet/ID` should display brevet with id `ID`.
		* POST `http://API:PORT/api/brevets` should insert brevet object in request into the database.
		* DELETE `http://API:PORT/api/brevet/ID` should delete brevet with id `ID`.
		* PUT `http://API:PORT/api/brevet/ID` should update brevet with id `ID` with object in request.

* Copy over `brevets/` from your completed project 5.
	* Replace every database related code in `brevets/` with calls to the new API.
		* Remember: AutoGrader will ensure there is NO CONNECTION between `brevets` and `db` services. `brevets` should only operate through `api` and still function the way it did in project 5.
		* Hint: Submit should send a POST request to the API to insert, Display should send a GET request, and display the last entry.
	* Remove `config.py` and adjust `flask_brevets.py` to use the `PORT` and `DEBUG` values specified in env variables (see `docker-compose.yml`).

* Update README.md with API documentation added.

As always you'll turn in your `credentials.ini` through Canvas.


## Authors

Fedi Aniefuna
