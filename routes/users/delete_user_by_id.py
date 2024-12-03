from flask import Blueprint, jsonify
from dependencies.users_db import users_collection #importing the database connection package

delete_user_by_id = Blueprint('delete_user', __name__)

@delete_user_by_id.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    '''
        Deleting the user by ID:
        - Checks if the user exists with the id
        - If uesr is present then delete it 
    '''
    try:
        # Check if user exists
        existing_user = users_collection.find_one({"id": id})
        if not existing_user:
            return jsonify({"error": "No user found with that ID"}), 404
        
        # Delete the user
        result = users_collection.delete_one({"id": id})
        if result.deleted_count == 1:
            return jsonify({"message": "User deleted successfully"}), 200
        
        # Fallback if user wasn't deleted for some reason
        return jsonify({"error": "Failed to delete user"}), 500
    
    except Exception as e:
        # Handle unexpected exceptions
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500
