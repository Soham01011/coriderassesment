from flask import Flask
from routes.user_routes import user_routes

app = Flask(__name__)

# Register Blueprint without a prefix
app.register_blueprint(user_routes, url_prefix="/users")  # Set prefix

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)