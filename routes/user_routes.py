from flask import Blueprint, request, jsonify
from dependencies.users_db import users_collection
from pydantic import ValidationError
from schemas.user_schema import UserCreate,UserResponce, UserUpdate
import uuid

user_routes = Blueprint('user_routes',__name__)

@user_routes.route("/users", methods=['GET'])
async def get_all_users():
    users = []
    async for user in users_collection.find({}):
        users.append(
            UserResponce(
                id = user["id"],
                username=user['username'],
                email = user['email']
            ).dict()
        )
    return jsonify(users), 200

@user_routes.route('/users/<id>', methods=['GET'])
async def get_user_by_id(id):
    print("got id "+ id)
    user = await users_collection.find_one({'id' : id})
    if user:
        print("user found"+ str(user))
        return jsonify(
            UserResponce(
                id = user['id'],
                username = user['username'],
                email=user['email']
            ).dict()
        ),200
    return jsonify({"error" : "usernot found with id "+id}), 404

@user_routes.route('/users', methods=['POST'])
async def create_user():
    try:
        # Validate request data using Pydantic schema
        print(request.json)
        user_data = UserCreate(**request.json)
        
        # Check for existing user
        existing_user = await users_collection.find_one({'username': user_data.username})
        if existing_user:
            return jsonify({"message": "User with the same username exists"}), 400
        
        # Insert new user
        user_dict = user_data.dict()
        await users_collection.insert_one(user_dict)

        return jsonify({"message": "User created successfully"}), 201
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

@user_routes.route('/users/<id>', methods=['PUT'])
async def update_user(id):
    try:
        user_data = UserUpdate(**request.json)  # Validate incoming data
        user_data_dict = user_data.dict(exclude_unset=True)  # Only include provided fields
        existing_user = await users_collection.find_one({'id': id})
        if not existing_user:
            return jsonify({"error": f"User not found with ID {id}"}), 404
        
        # Update the user's data in the database
        await users_collection.update_one(
            {'id': id},
            {'$set': user_data_dict}
        )
        return jsonify({"message": "User updated successfully"}), 200
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
    
@user_routes.route('/users/<id>', methods=['DELETE'])
async def delete_user(id):
    print("id to be deleted" , id)
    result = await users_collection.delete_one({'id': id})
    if result.deleted_count == 0:
        return jsonify({"error": "User not found with ID " + id}), 404
    return jsonify({"message": "User deleted successfully"}), 200
    