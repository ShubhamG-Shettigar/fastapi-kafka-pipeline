from fastapi import FastAPI, Header, HTTPException
from app.services.auth_service import verify_token, hash_password, verify_password, create_access_token
#from kafka_producer import send_to_kafka
#from pydantic import BaseModel
import uuid
from app.kafka_client.producer import producer, publish_events
from app.db.postgres import conn, cursor
from app.routes.auth_routes import router as auth_router
from app.models.schemas import User

app = FastAPI()
app.include_router(auth_router, prefix="/auth")

@app.post("/send")
async def publish_events(data: User):
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