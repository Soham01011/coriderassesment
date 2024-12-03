from pydantic import ValidationError
from schemas.user_schema import UserResponce # importing schema to return data properly
from flask import Blueprint, jsonify
from dependencies.users_db import users_collection #importing the database

get_users_route = Blueprint("get_users", __name__)

@get_users_route.route("/users", methods=["GET"])
def get_users():
    '''
        Get all users:
        - A simple Get request to return all the users
    '''
    try:
        return_users = []
        cursor = users_collection.find()
        for user in cursor:
            try:
                user_response = UserResponce(**user)
                return_users.append(user_response.dict())
            except ValidationError as e:
                return jsonify({"error": "Validation Error", "details": e.errors()}), 400

        return jsonify({"message": return_users}), 200

    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500
