
# Flask API with MongoDB

This project contains a Flask API that connects to a MongoDB database. The API allows you to perform CRUD operations (Create, Read, Update, Delete) for user data.

## Features

- User registration and authentication
- User data retrieval
- User data updating and deletion



## Requirements
Before running the application, ensure you have the following installed:

- Python 3.12+
- Docker
- Docker Compose


## Run Locally

Clone the project

```bash
  git clone https://github.com/Soham01011/coriderassesment
```

Go to the project directory

```bash
  cd coriderassesment
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Start the server

```bash
  python app.py
```


## Docker Container

To build docker container

```bash
  docker-compose build
  docker pull mongo:latest
  docker-compose up
```



## Running Tests

After spinning up the containers or running locally on the server you test it by making api calls at http://127.0.0.1:5000/api/users

1] Creating User (POST):
  /users
```json
   {
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepassword"
   }
```

2] Get user (GET):    /users

3] Get user by id (GET): /users/id
```json
  {
    "username": "john_doe_updated",
    "email": "john_updated@example.com",
    "password": "newsecurepassword"
  }
```

4] Delete user by id (DELETE): /users/id

5] Update user details by id (PUT): /users/id
```json
{
  "username": "john_doe_updated",
  "email": "john_updated@example.com",
  "password": "newsecurepassword"
}
```

