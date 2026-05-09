from fastapi import FastAPI
from kafka_producer import send_to_kafka
from pydantic import BaseModel

class User(BaseModel):
    name: str
    surname: str
    
    
app = FastAPI()


@app.post("/send")
async def send_data(data: User):
    
    send_to_kafka("shubham", data.dict())

    return {
        "status": "sent to kafka",
        "data": data
    }