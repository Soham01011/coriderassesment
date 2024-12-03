from pydantic import ValidationError
from schemas.user_schema import UserResponce
from flask import Blueprint, jsonify
from dependencies.users_db import users_collection

get_users_route = Blueprint("get_users", __name__)

@get_users_route.route("/users", methods=["GET"])
def get_users():
    try:
        return_users = []
        # Iterate over the cursor returned by find()
        cursor = users_collection.find()
        for user in cursor:
            try:
                # Validate each user document
                user_response = UserResponce(**user)
                return_users.append(user_response.dict())
            except ValidationError as e:
                # Handle validation errors
                return jsonify({"error": "Validation Error", "details": e.errors()}), 400

        # Return the list of users
        return jsonify({"message": return_users}), 200

    except Exception as e:
        # Handle general errors
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500
