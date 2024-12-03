from pydantic import ValidationError
from flask import Blueprint, jsonify, request
from dependencies.hashing import hash_password
from dependencies.users_db import users_collection
from schemas.user_schema import UserUpdate, UserResponce

update_user_route = Blueprint("update_user", __name__)

@update_user_route.route("/users/<id>", methods=['PUT'])
def update_user(id):
    try:
        # Parse and validate incoming data
        user_data = UserUpdate(**request.json)

        # Check if the user exists
        existing_user = users_collection.find_one({"id": id})
        if not existing_user:
            return jsonify({"message": "Incorrect ID"}), 404
        
        # Prepare update data and update the user
        update_data = user_data.dict(exclude_unset=True)
        result = users_collection.update_one({"id": id}, {"$set": update_data})

        # Confirm the update was successful
        if result.modified_count == 1:
            updated_user = users_collection.find_one({"id": id})
            if updated_user:
                user_response = UserResponce(**updated_user)
                return jsonify({"message": user_response.dict()}), 200
        else:
            return jsonify({"message": "No changes were made"}), 400

    except ValidationError as e:
        # Handle validation errors
        return jsonify({"error": e.errors()}), 400

    except Exception as e:
        # Handle any unexpected errors
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500
