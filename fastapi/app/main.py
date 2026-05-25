from fastapi import FastAPI, Header, HTTPException
from services.auth import verify_token, hash_password, verify_password, create_access_token
#from kafka_producer import send_to_kafka
from pydantic import BaseModel
import uuid
from kafka_client.producer import producer, send_to_kafka
from db.postgres import conn, cursor

class User(BaseModel):
    name: str
    surname: str

class UserSignup(BaseModel):
    username: str
    password: str
    
class UserLogin(BaseModel):
    username: str
    password: str
    
app = FastAPI()


@app.post("/send")
async def send_data(data: User):
    data = data.dict()
    data["message_id"] = str(uuid.uuid4())
    send_to_kafka("orders", data)

    return {
        "status": "sent to kafka",
        "data": data
    }   
    
@app.get("/protected")
def protected_route(authorization: str = Header(None)):
    print(authorization)
    try:
        if not authorization:
            raise Exception("Missing Auth Header")
        scheme, token = authorization.split()
        #print("Scheme", scheme)
        #print("token", token)
        payload = verify_token(token)

        return {
            "message": "Protected route accessed",
            "payload": payload
        }

    except Exception as e :
        print(e)
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )
        
#cursor = conn.cursor()   
@app.post("/signup")
def signup(user: UserSignup):
    hashed =hash_password(user.password)
    print("Password Hashed")
    
    cursor.execute("Insert into auth_users (username, password) values (%s, %s)", (user.username, hashed))
    try:
        conn.commit()
    except:
        conn.rollback()
    print("Hashed password stored in DB")
    return{"message":"User registered successfully"}
    
    
@app.post("/login")
def login(user: UserLogin):
    cursor.execute("Select password from auth_users where username=%s", (user.username,))
    result = cursor.fetchone()
    if not result:
        return {"message":"User not found"}
    stored_hash = result[0]
    is_valid = verify_password(user.password, stored_hash)
    if not is_valid:
        return {"message":"Invalid password"}
    token = create_access_token({"sub":user.username})
    return {"access_token": token}