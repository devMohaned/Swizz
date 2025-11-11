from fastapi import FastAPI

from config.settings import settings
from core.logging import configure_logging
from controller import users_controller
from db.database import Base, engine
from exception.exception_handler import *
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
    openapi_url=openapi_url,
)

# Database Initialization (Creation)
Base.metadata.create_all(bind=engine)

# Routers
app.include_router(users_controller.router, prefix="/api")

# Middlewares
app.add_middleware(RequestIdMiddleware)

# Exception Handlers
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, general_http_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

@app.get("/healthz")
def healthz(): return {"ok": True}
