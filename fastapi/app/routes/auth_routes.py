from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel
from db.postgres import conn, get_cursor, get_db
from services.auth_service import (
    hash_password,
    verify_password,
    create_access_token,
    verify_token, create_user
)
import asyncio, time


class UserSignup(BaseModel):
    username: str
    password: str
    
class UserLogin(BaseModel):
    username: str
    password: str

router = APIRouter()


def send_email():
    print("Task started")
    for i in range(10):
        print(i)
    print("Sending email...")

#Testing async operations
@router.get("/test-async")
async def test_async():
    import time
    print(f"Start: {time.time()}")
    await asyncio.sleep(10)
    print(f"End: {time.time()}")
    return {"message": "done"}
    
    
    
@router.post("/signup")
async def signup(user: UserSignup, background_tasks:BackgroundTasks, cursor = Depends(get_db)):
    print("Signup route hit")
    background_tasks.add_task(send_email)
    try:
        create_user(user, cursor)
    except Exception as e:
        conn.rollback()
        return {"error": str(e)}
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