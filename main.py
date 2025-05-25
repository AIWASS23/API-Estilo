from fastapi import FastAPI

from app.routes.order_routes import order_router
from app.routes.product_routes import product_router
from app.routes.user_routes import user_router
from app.routes.client_routes import client_router


# rodar na raiz
#alembic revision --autogenerate -m "create <SCHEMA> table" EX: create clients table
#alembic upgrade head

app = FastAPI()
app.include_router(user_router)
app.include_router(client_router)
app.include_router(product_router)
app.include_router(order_router)