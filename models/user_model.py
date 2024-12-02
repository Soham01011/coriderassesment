import uuid

class UserModel:
    def __init__(self, username: str, password: str, email: str):

        self.id = str(uuid.uuid4())
        self.username = username
        self.password = password 
        self.email = email

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "password": self.password  
        }
