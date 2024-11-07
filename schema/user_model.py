'''
    Libraries used :
        datetime to store when the user account was created
        re to sanitize and check the inputs to avoid injection of malicious code
        bcrytp to hash the password
        uuid to generate a random id for each user
'''
from datetime import datetime
import re 
import uuid 
import bcrypt

class usersSchema: 
    # here we createing a class to hold the regular expressions 
    _patterns = {
        "username": re.compile(r"^[a-zA-Z0-9]{3,15}$"),
        "email" : re.compile(r"^[\w\.-]+@[\w\.-]+\.\w{2,4}$"),
        "password" : re.compile(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@#$%^&+=!]{8,25}$")
    }

    # init function takes the arguments as username email and password. Thus checking them and creating a structure so it is safe
    # to put data into the mongodb
    def __init__(self, username, email=None, password=None):

        if not self._patterns["username"].match(username):
            raise ValueError("Invalid username. Must be alphanumeric and character length 3-15")
        
        if email and not self._patterns["email"].match(email):
            raise ValueError("Invalid email format")
  
        if password and not self._patterns["password"].match(password):
            raise ValueError("Password must contain minimum 8, max 25 characters long, with at least one number and one letter")

        userid = uuid.uuid4()
        hashed_pwd = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()) if password else None
        
        self.data = {
            "username": username,
            "email": email,
            "password": hashed_pwd.decode('utf-8') if hashed_pwd else None,
            "created_at": datetime.now().isoformat(),
            "userID": str(userid)
        }

    #Since the init function cant return this funciton is created to return the data
    def return_data(self):
        return self.data
