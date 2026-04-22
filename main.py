from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.routes import base,data
from src.utils.config import get_settings

app_settings = get_settings()

@asynccontextmanager
async def life_span(app: FastAPI):
    #add any startup code here
    print("Starting up...")
    yield
    print("Shutting down...")


app = FastAPI(
    title=app_settings.app_name,
    version=app_settings.app_version,
    description=app_settings.app_description,
    lifespan=life_span,
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
    openapi_url="/api/v1/openapi.json"
)

app.include_router(base.router) #base router for root and health check endpoints
app.include_router(data.router) #data router for file upload and other data related endpoints