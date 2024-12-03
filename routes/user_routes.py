from flask import Blueprint
from .users.create_user_route import create_users_route  #create user SubRoute      POST
from .users.update_user_route import update_user_route   #update user SubRoute      PUT
from .users.get_users_route import get_users_route       #get user details SubRoute GET
from .users.get_user_by_id import get_users_by_id        #get user details by id    GET
from .users.delete_user_by_id import delete_user_by_id   #delete user account       DELETE

user_routes = Blueprint('user_routes', __name__)

# Registering routes for CRUD operations on users collection
user_routes.register_blueprint(create_users_route)
user_routes.register_blueprint(update_user_route)
user_routes.register_blueprint(get_users_route)
user_routes.register_blueprint(get_users_by_id)
user_routes.register_blueprint(delete_user_by_id)