import bcrypt

def hash_password(password: str)-> str:
    salt = bcrypt.gensalt()
    hashed_pwd = bcrypt.hashpw(password.encode('utf-8'),salt)
    return hashed_pwd.decode('utf-8')

def verify_password(password: str)-> str:
    pass # password verification if login was there