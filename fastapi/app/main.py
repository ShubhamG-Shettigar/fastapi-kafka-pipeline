from fastapi import FastAPI, Header, HTTPException
from app.routes.auth_routes import router as auth_router
from app.db.postgres import create_orders_table

app = FastAPI(title="Event Driven Backend")
create_orders_table()
app.include_router(auth_router, prefix="/auth")

@app.get("/protected")
def protected_route(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Missing authorization header"
        )
    return {
        "message": "Protected route accessed"
    }