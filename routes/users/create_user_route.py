from pydantic import ValidationError
from models.user_model import UserModel
from dependencies.hashing import hash_password
from flask import Blueprint, request, jsonify
from dependencies.users_db import users_collection
from schemas.user_schema import UserCreate, UserResponce, UserCreateRequest

create_users_route = Blueprint("create_user", __name__)

@create_users_route.route("/users", methods=['POST'])
def create_user():
    try:
        # Validate input data using Pydantic
        user_data = UserCreateRequest(**request.json)

        # Hash the password before creating the user model
        hashed_password = hash_password(user_data.password)
        
        # Create a UserCreate instance with hashed password
        user_create = UserCreate(
            username=user_data.username,
            email=user_data.email,
            password=hashed_password
        )

        # Check if the user already exists
        existing_user = users_collection.find_one({'username': user_create.username})
        if existing_user:
            return jsonify({"message": "User with username already exists"}), 400

        # Create a new user model instance
        new_user = UserModel(
            username=user_create.username,
            password=user_create.password,
            email=user_create.email
        )

        # Insert the new user into the database
        users_collection.insert_one(new_user.to_dict())

        # Fetch the created user for confirmation
        created_user = users_collection.find_one({"username": user_create.username})
        if created_user:
            user_response = UserResponce(**created_user)
            return jsonify(user_response.dict()), 201

        return jsonify({"error": "Error creating the user"}), 500

    except ValidationError as e:
        # Handle validation errors
        return jsonify({"error": e.errors()}), 400

    except Exception as e:
        # Handle any other exceptions
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500
