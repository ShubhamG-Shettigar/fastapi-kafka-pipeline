from fastapi import APIRouter, HTTPException, Depends
from app.models.schemas import MessageResponse, UserSignup, UserLogin
from app.services.auth_service import (
    hash_password,
    verify_password,
    create_access_token
)
from app.db.postgres import get_db

router = APIRouter()
@router.post("/signup", response_model=MessageResponse)
def signup(user: UserSignup, connection=Depends(get_db)):
    cursor = connection.cursor()
    try:
        hashed_password = hash_password(user.password)
        cursor.execute(
            """
            INSERT INTO auth_users (username, password)
            VALUES (%s, %s)
            """,
            (user.username, hashed_password)
        )
        connection.commit()
        return {"message": "User registered successfully"}
    except Exception:
        connection.rollback()
        raise HTTPException(
            status_code=400,
            detail="User already exists"
        )
    finally:
        cursor.close()
        
@router.post("/login")
def login(user: UserLogin, connection=Depends(get_db)):
    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            SELECT password
            FROM auth_users
            WHERE username = %s
            """,
            (user.username,)
        )
        result = cursor.fetchone()
        if not result:
            return {"message": "User not found"}
        stored_hash = result[0]
        if not verify_password(user.password, stored_hash):
            return {"message": "Invalid password"}
        token = create_access_token(
            {"sub": user.username}
        )
        return {"access_token": token}
    finally:
        cursor.close()