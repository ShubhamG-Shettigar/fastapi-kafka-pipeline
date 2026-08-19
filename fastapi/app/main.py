from fastapi import FastAPI
from app.routes.auth_routes import router as auth_router
from app.routes.order_routes import router as order_router
from app.db.postgres import create_orders_table

app = FastAPI(title="Event Driven Backend")
create_orders_table()
app.include_router(auth_router, prefix="/auth")
app.include_router(order_router)
