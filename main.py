import sentry_sdk
from fastapi import FastAPI

from app.config import settings
from app.routes.order_routes import order_router
from app.routes.product_routes import product_router
from app.routes.user_routes import user_router
from app.routes.client_routes import client_router

if settings.SENTRY_DSN:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        traces_sample_rate=1.0,
    )

app = FastAPI()
app.include_router(user_router)
app.include_router(client_router)
app.include_router(product_router)
app.include_router(order_router)