# Capstone Full Stack Project

## Remote Host URL

https://akueisara-capstone.herokuapp.com/ 

## Motivations

Working on this project is an opportunity for me to reinforce those skills and walk away very confident in them.

- Coding in Python 3
- Relational Database Architecture
- Modeling Data Objects with SQLAlchemy
- Internet Protocols and Communication
- Developing a Flask API
- Authentication and Access
- Authentication with Auth0
- Authentication in Flask
- Role-Based Access Control (RBAC)
- Testing Flask Applications
- Deploying Applications

## Casting Agency Specifications
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

- Models:

    - Movies with attributes title and release date
    - Actors with attributes name, age and gender
- Endpoints:

    - GET /actors and /movies
    - DELETE /actors/ and /movies/
    - POST /actors and /movies and
    - PATCH /actors/ and /movies/
- Roles:

    - Casting Assistant
        - Can view actors and movies
    - Casting Director
        - All permissions a Casting Assistant has and…
        - Add or delete an actor from the database
        - Modify actors or movies
        - Executive Producer
        - All permissions a Casting Director has and…
        - Add or delete a movie from the database

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server locally

From within the `./src` directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=app.py
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## Testing
To run the tests, run
```
dropdb capstone_test
createdb capstone_test
psql capstone_test < capstone_test.psql
python test_app.py
```


## API Reference

### Getting Started

- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration.
- Authentication 
    - Log in to https://akueisara.us.auth0.com/authorize?audience=capstone&response_type=token&client_id=T97NR87FuUeqlZecylQw8A8YnoulGJe6&redirect_uri=http://localhost:8080 to get the access token
    - Add the header `Authorization`: `Bearer your_access_token` to the request

### Error Handling

Errors are returned as JSON objects in the following format:

```
{
    "success": False,
    "error": 404,
    "message": "resource not found"
}
```

The API will return these error types when requests fail:

- 400: Bad Request
- 401: Unauthorized
- 404: Resource Not Found
- 405: Method Not Allowed
- 422: Not Processable

### Endpoints 

#### GET /movies

- Returns a list of all the movies and a number of total movies.
- Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.

#### POST /movies

- Creates a new movie using the title and release date. 
- Returns the ID of the created movie, success value, and a movie list with the created movie

#### UPDATE /movies/{movie_id}

- Updates the movie based on the given movie ID using the updated title and release date.
- Returns the success value and a list with the updated movie.

#### DELETE /movies/{movie_id}

- Deletes the movie based on the given movie ID.
- Returns the success value, the ID of the deleted movie, the list of all the movies, and the number of total movies.

#### GET /actors

- Returns a list of all the actors and a number of total actors.
- Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.

#### POST /actors

- Creates a new actor using the name, age, and gender. 
- Returns the ID of the created actors, success value, and a actor list with the created actor

#### UPDATE /actors/{actor_id}

- Updates the actor based on the given actor ID using the updated name, age, and gender.
- Returns the success value and a list with the updated actor.

#### DELETE /actors/{actor_id}

- Deletes the actor based on the given actor ID.
- Returns the success value, the ID of the deleted actor, the list of all the actors, and the number of total actors.
