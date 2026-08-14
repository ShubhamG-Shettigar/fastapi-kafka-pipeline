from pydantic import BaseModel
    
class UserSignup(BaseModel):
    username: str
    password: str
    
class UserLogin(BaseModel):
    username: str
    password: str

class User(BaseModel):
    name: str
    surname: str
    
class MessageResponse(BaseModel):
    message: str