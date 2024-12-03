from pydantic import ValidationError
from models.user_model import UserModel # package to import the UserModel to structure input data
from dependencies.hashing import hash_password # importing hashing function as a module
from flask import Blueprint, request, jsonify
from dependencies.users_db import users_collection  #importing the database connection
from schemas.user_schema import UserCreate, UserResponce, UserCreateRequest #importing user imputing formating and checking

create_users_route = Blueprint("create_user", __name__) 

@create_users_route.route("/users", methods=['POST'])
def create_user():
    """
        Functions it preforms:
        - Validates the user imputs
        - hashing the password
        - fomating the inputs
        - check if the user already exists
        - then insert the data
    """
    try:
        # Validate input data using Pydantic
        user_data = UserCreateRequest(**request.json)

        hashed_password = hash_password(user_data.password)
        
        user_create = UserCreate(
            username=user_data.username,
            email=user_data.email,
            password=hashed_password
        )

        existing_user = users_collection.find_one({'username': user_create.username})
        if existing_user:
            return jsonify({"message": "User with username already exists"}), 400

        new_user = UserModel(
            username=user_create.username,
            password=user_create.password,
            email=user_create.email
        )

        users_collection.insert_one(new_user.to_dict())

        # Fetch the created user for confirmation
        created_user = users_collection.find_one({"username": user_create.username})
        if created_user:
            user_response = UserResponce(**created_user)
            return jsonify(user_response.dict()), 201

        return jsonify({"error": "Error creating the user"}), 500

    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500
