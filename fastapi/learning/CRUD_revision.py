import sqlite3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import List


class post(BaseModel):
    name: str
    email: EmailStr
    age: int
    networth: float
    
class pull(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: int
    networth : float
    

connection = sqlite3.connect("revisionn.db")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE if not exists shubhamm(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email Varchar(255), age int, networth float)
""")
connection.commit()


app = FastAPI()
@app.get("/database", response_model = List[pull])
async def database():
    cursor.execute("Select * from shubhamm")
    rows = cursor.fetchall()
    returnlist = []
    for row in rows:
        returnlist.append({"id": row[0], "name": row[1], "email": row[2], "age": row[3], "networth" : row[4]})
    return returnlist
    
@app.post("/postdata", response_model = pull)
async def postdata(item: post):
    cursor.execute("Insert into shubhamm (name, email, age, networth) values (?, ?, ?, ?)", (item.name, item.email, item.age, item.networth))
    connection.commit()
    return {"id":cursor.lastrowid, "name": item.name, "email": item.email, "age": item.age, "networth": item.networth}
    
    
@app.put("/putdata/{item_id}")
async def putdata(item_id: int, item: post):
    cursor.execute("Update shubhamm set name=? where id=?", (item.name, item_id))
    connection.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code = 404, detail = "The item was not found")
    print("DataUpdated")
    return {"id":item_id, "name":item.name}
    
  
  
@app.delete("/deletedata/{item_id}")
async def deletedata(item_id: int):
    cursor.execute("Delete from shubhamm where id=?", (item_id,))
    connection.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code = 404, detail = "Item not found")
    print("Data deleted")
    return {"status":"success", "Data":{"id": item_id, "message": f"{item_id} was deleted successfully"}}
    