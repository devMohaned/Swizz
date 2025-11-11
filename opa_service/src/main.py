from fastapi import FastAPI

from config.settings import settings
from controller import internal_controller
from core.logging import configure_logging
from exceptions.exception_handler import *
from middleware.request_id import RequestIdMiddleware

# Initialize logging using settings
configure_logging()

# Application's API
is_prod = settings.environment.lower() == "prod"
docs_url = None if is_prod else "/docs"
redoc_url = None if is_prod else "/redoc"
openapi_url = None if is_prod else "/openapi.json"

app = FastAPI(
    title=settings.app_name,
    debug=settings.log_level.lower() == "debug",
    docs_url=docs_url,
    redoc_url=redoc_url,
    openapi_url=openapi_url
)

# Middleware + Routers
app.add_middleware(RequestIdMiddleware)
app.include_router(internal_controller.router)

# Exception Handler
app.add_exception_handler(Exception, general_exception_handler)


@app.get("/health")
async def health():
    return {"status": "healthy"}
