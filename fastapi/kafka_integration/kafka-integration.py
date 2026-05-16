from fastapi import FastAPI
from kafka_producer import send_to_kafka
from pydantic import BaseModel
import uuid

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