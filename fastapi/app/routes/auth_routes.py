from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from db.postgres import conn, get_cursor
from services.auth import (
    hash_password,
    verify_password,
    create_access_token,
    verify_token
)


class UserSignup(BaseModel):
    username: str
    password: str
    
class UserLogin(BaseModel):
    username: str
    password: str

router = APIRouter()

@router.post("/signup")
def signup(user: UserSignup):
    cursor = get_cursor()
    hashed =hash_password(user.password)
    print("Password Hashed")
    
    cursor.execute("Insert into auth_users (username, password) values (%s, %s)", (user.username, hashed))
    try:
        conn.commit()
    except:
        conn.rollback()
        #return {Exception}
    print("Hashed password stored in DB")
    return{"message":"User registered successfully"}
    
    
@router.post("/login")
def login(user: UserLogin):
    cursor = get_cursor()
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