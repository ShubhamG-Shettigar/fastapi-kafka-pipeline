from fastapi import FastAPI, Header, HTTPException
from services.auth import verify_token
#from kafka_producer import send_to_kafka
from pydantic import BaseModel
import uuid
from kafka_client.producer import producer, send_to_kafka


class User(BaseModel):
    name: str
    surname: str
    
    
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
def protected_route(authorization: str):
    print(authorization)
    try:

        scheme, token = authorization.split()
       # print("Scheme", scheme)
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