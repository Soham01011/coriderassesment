from flask import Blueprint
from .users.create_user_route import create_users_route  # Import create user route
from .users.update_user_route import update_user_route  # Import update user route
from .users.get_users_route import get_users_route
from .users.get_user_by_id import get_users_by_id
from .users.delete_user_by_id import delete_user_by_id

user_routes = Blueprint('user_routes', __name__)

# Registering routes for creating and updating users
user_routes.register_blueprint(create_users_route)
user_routes.register_blueprint(update_user_route)
user_routes.register_blueprint(get_users_route)
user_routes.register_blueprint(get_users_by_id)
user_routes.register_blueprint(delete_user_by_id)