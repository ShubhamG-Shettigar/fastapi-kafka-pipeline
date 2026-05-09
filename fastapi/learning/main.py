from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

class Item(BaseModel):
    name: str
    price: float
    
    
    
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello Fartyyyyy 🚀"}
    
    
    
@app.get("/greet/{name}")
def getname(name : str):
    return {f"hello jaan {name}"}
    
    
@app.get("/result")
def getresult(a: int, b: int):
    return {"Brother your result iss": a+b}
    

itemm = [{"name":"ss","price":10.0}]
#itemm = []
@app.post("/item")
def create_item(item: Item):
    itemm.append(item)
    return {"Khammagni, tohar menu etthe he": itemm}
    # return {"item you posted is": itemm}
    
@app.get("/item", response_model=dict[Item])
def getitems():
    return {"Your menu is": itemm}
    #return itemm
    
@app.get("/item/{name}")
def getitems(name: str):
    for g in itemm:
        if g.name.lower() == name.lower():
            return {f"Price of {name} is {g.price}"}
    return {"Not found"}
    #return {f"item {name} has is": itemm}