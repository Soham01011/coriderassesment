from flask import Flask
from routes.user_routes import user_routes

app = Flask(__name__)

app.register_blueprint(user_routes, url_prefix="/api")  #creting route API for sub routes of users

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True) # setting host ip to run on docker container