'''
CO RIDER ASSESMENT
    importing the libariries:
        Flask for the API
        pymongo for mongodb client connection
        os and dotenv to load environment variables which can be given before running the docker image
        bcrypt to hash the users passwords
        usersSchema is a class which constructs the schema
'''
from flask import Flask, request , jsonify, render_template, redirect, url_for
from pymongo import MongoClient
from pymongo.errors import PyMongoError
import os 
import re
import bcrypt
from dotenv import load_dotenv

from schema.user_model import usersSchema

load_dotenv()

app = Flask(__name__)

client = MongoClient(os.getenv("MONGODB_URI"))
db = client[os.getenv("DATABASE")]
users_coll = db[os.getenv("COLLECTION")]

'''
    This route can only accept GET and POST methods and fetch users list and create more users
'''
@app.route("/users", methods=["GET","POST"])
def handelUsers():
    if request.method == "GET":
        users = list(users_coll.find())
        if users:
            for user in users:
                user.pop('_id', None)  
                user.pop('password',None)
            return jsonify(users), 200
        else:
            return jsonify({"message": "No user data"}), 200
    elif request.method == "POST":
        try:          
            user_data = usersSchema(**request.json) #the data entered by the user via the API call is passed the usersSchema to validate the inputs 

            # checking if the username already exists in the database
            existing_user = users_coll.find_one({"username": user_data.data["username"]})
            if existing_user:
                return jsonify({"error": "Username already exists"}), 409 
            
            users_coll.insert_one(user_data.return_data())

            return jsonify({"message" : str("Data inserted"), "userID" :user_data.return_data()["userID"] }), 201 #the user id is
            # passed to the frontend so that if the user reaches another route the userid can be submitted and fetch the relative
            # data. OR can be done by validating the user and providing the session token instead of the userID.
        except ValueError as e :
            return jsonify({ "error" : str(e)}), 400
        except PyMongoError :
            return jsonify({"error" : "Internal server error"}),500
        

'''
    This route created to accepet the userid from the query parameters to work with GET ,PUT ,DELETE methods to perform reading ,
    updation , deletion operations. Reason for creating such ruote to manage the request regarding the CRUD operations and help 
    to manage the incoming requests.
'''
@app.route("/users/<userid>", methods=["GET", "PUT", "DELETE"])
def handelUserID(userid):
    if not re.match(r"^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-4[a-fA-F0-9]{3}-[89abAB][a-fA-F0-9]{3}-[a-fA-F0-9]{12}$", userid):
        return jsonify({"error": "Invalid user ID format"}), 400
    if request.method == "GET":
        user_data = users_coll.find_one({"userID": userid}) # fetches the user data with the user
        user_data.pop("_id", None)
        user_data.pop("password", None)
        if user_data:
            return jsonify(user_data), 200
        else:
            return jsonify({"error": "User not found in database"}), 404
    
    elif request.method == "PUT":
        data = request.json
        update_fields = {}

        if "username" in data:         
            if not usersSchema._patterns["username"].match(data["username"]):

                existing_user = users_coll.find_one({"username": user_data.data["username"]})
                if existing_user:

                    return jsonify({"error": "Username already exists"}), 409 
                
                return jsonify({"error": "Invalid username format. Must be alphanumeric and length of 3 - 15"}), 400
            
            update_fields["username"] = data["username"]

        if "email" in data: 

            if not usersSchema._patterns["email"].match(data["email"]):

                return jsonify({"error": "Invalid email format"}), 400
            
            update_fields["email"] = data["email"]

        if"password" in data:

            if not usersSchema._patterns["password"].match(data["email"]):

                return jsonify({"error" : "Password must contain minimum 8 charecters long, with atleast one number and letter"})
            
            update_fields["password"] = data["password"]
        
        if not update_fields: 
            return jsonify({"error": "No data to update"}), 400
        try:
            result = users_coll.update_one({"userID": userid}, {"$set": update_fields})
        except PyMongoError :
            return jsonify({"error" : "Internal server error"}), 500

        if result.matched_count == 0:
            return jsonify({"error": "User not found"}), 404

        return jsonify({"message": "User details updated successfully"}), 200
                    
    elif request.method == "DELETE":
        result = users_coll.delete_one({"userID": userid})
        if result.deleted_count == 0:
            return jsonify({"error": "User not found"}), 404
        return jsonify({"message": "User deleted successfully"}), 200
    
'''
    Here are some extra routes with the webpages to visualize the data. I have user Jinga code to render the webpages.
'''
    
@app.route("/displayusers", methods=["GET"])
def displayusers():
    if request.method == "GET":
        users = list(users_coll.find())
        if users:
            for user in users:
                user.pop('_id', None)  
                user.pop('password',None)
            return render_template("users.html", all_users = users ), 200
        else:
            return render_template("users.html", error="No user found" )
        
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    
    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        try:
            usersSchema(username=username, password=password, email='')
            user = users_coll.find_one({"username": username})

            if user:
                if bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
                    return redirect(url_for('displayusers')) 
                else:
                    return redirect(url_for('login'))
            else:
                return redirect(url_for('login'))

        except ValueError as e:
            return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


