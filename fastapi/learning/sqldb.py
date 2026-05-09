import sqlite3
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastapi import HTTPException


class Push(BaseModel):
    name: str
    price: float
    
class Pull(BaseModel):
    idd: int
    name: str
    price: float
    
    
conn = sqlite3.connect("items.db")
cursor = conn.cursor()

cursor.execute(
    """
    CREATE TABLE if not exists shubham(
 
    name TEXT,
    price float
    )
    
    """
)

# cursor.execute("Select name from sqlite_master where type='table';")
# print(cursor.fetchall())
conn.commit()

app = FastAPI()
@app.post("/items", response_model = Pull)
async def postitems(item: Push):
    cursor.execute
   (
        "Insert into shubham (name, price) values (?,?)", (item.name, item.price)
    )
    conn.commit()
    
    return {"idd":cursor.lastrowid, "name":item.name, "price":item.price}
    
    
@app.get("/itemcall",response_model = List[Pull])
async def getitems():
    cursor.execute("Select * from shubham")
    rows = cursor.fetchall()
    itemlist = []
    for row in rows:
        itemlist.append({
            "price": row[2],
            "idd":row[0],
            "name": row[1],
            "dave": 10
        })
    return itemlist
    
    
    
@app.put("/items/{item_id}")
async def putitems(item_id: int, item: Push):
    cursor.execute("Update shubham set name = ?, price = ? where id = ?",(item.name, item.price, item_id))
    conn.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code = 204, detail = "Itcemvv not found")
    return {"id": item_id, "name": item.name, "price": item.price}
    
    
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    cursor.execute("DELETE FROM shubham WHERE id = ?", (item_id))
    conn.commit()

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Item not found")

    return {"message": "Item deleted successfully"}
    
    