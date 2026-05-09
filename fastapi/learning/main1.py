from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel

app = FastAPI()

items = {}
class Item(BaseModel):
    name: str
    price: float
    
@app.post("/items")
def create_item(item: Item):
    item_id = len(items) + 1
    items[item_id] = item
    return {"id": item_id, "Item created": item}
    
    
@app.put("/items/{item_id}", status_code = status.HTTP_201_CREATED)
def put_item(item_id: int, item: Item):
    if item_id in items:
        items[item_id] = item
        return {"message": f"Item with {item_id} is updated", "Here is the final list": items}
        
    else:
        items[item_id] = item
        return {"message": f"Item created with {item_id}"}

@app.delete("/items/{item_id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_item(item_id:int):
    if item_id in items:
        del items[item_id]
        return {f"Item with {item_id} is deleted successfully"}
    else:
        raise HTTPException(status_code = 404, detail="The item was not found")

@app.get("/items")
def get_items():
    return {"Nimma items list": items}
    
@app.get("/humnava/{humnava}")
def get_humnava(humnava:str):
    return {f"nimma priti na hesaru {humnava}"}
    
@app.get("/humnava")
def gethu(limit:int = 10):
    return {f"Nimma limit {limit} ishte"}
    