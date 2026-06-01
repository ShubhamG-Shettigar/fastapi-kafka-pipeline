#for storing hashed password
from passlib.context import CryptContext
from db.postgres import conn
#for JWT tokens
from datetime import datetime, timedelta
from jose import jwt

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")
SECRET_KEY = "shubham"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)
    return encoded_jwt
    
def verify_token(token: str):
    payload =jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
    return payload
    
def create_user(user, cursor):
    hashed = hash_password(user.password)
    print("Password Hashed")
    cursor.execute(
        "Insert into auth_users (username, password) values (%s, %s)",
        (user.username, hashed)
    )
    
    