from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
#from pydantic import BaseModel
from app.db.postgres import conn, get_cursor, get_db
from app.models.schemas import MessageResponse, UserSignup, UserLogin
from app.services.auth_service import (
    hash_password,
    verify_password,
    create_access_token,
    verify_token, create_user
)
from psycopg2.errors import UniqueViolation
import asyncio, time
from app.kafka_client.producer import publish_events

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
       
    
@router.post("/signup", response_model=MessageResponse)
async def signup(user: UserSignup, background_tasks:BackgroundTasks, cursor = Depends(get_db)):
    #print("Signup route hit")
    background_tasks.add_task(send_email)
    try:
        publish_events("signup-events", {"username" : user.username, "password": user.password})
    except UniqueViolation:
        conn.rollback()
        #return {"error": str(e)}
        raise HTTPException(status_code= 400, detail = "User already exists")
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code = 500, detail= str(e))
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