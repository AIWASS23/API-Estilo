from fastapi import FastAPI
from app.routes.user_routes import user_router as auth_router
from app.routes.client_routes import client_router

# rodar na raiz
#alembic revision --autogenerate -m "create <SCHEMA> table" EX: create clients table
#alembic upgrade head

app = FastAPI()
app.include_router(auth_router)
app.include_router(client_router)