from pydantic import ValidationError
from schemas.user_schema import UserResponce
from flask import Blueprint, jsonify
from dependencies.users_db import users_collection

get_users_by_id = Blueprint("user_by_id", __name__)

@get_users_by_id.route("/users/<id>", methods=['GET'])
def get_user_by_id(id):
    '''
        Get user by ID :
        - The id will be passed in the api call
        - Search of the user in the collection with the id
        - If user found then parse the data with UserResponce ouput schema
    '''
    try:
        existing_user = users_collection.find_one({"id": id})
        if not existing_user:
            return jsonify({'message': 'No user found with that ID'}), 404

        # Validate and return user data using Pydantic
        existing_user = UserResponce(**existing_user)
        return jsonify({"message": existing_user.dict()}), 200

    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500
