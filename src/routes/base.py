from fastapi import APIRouter,Depends
from src.utils.config import get_settings,Settings

router = APIRouter(
    prefix="/api/v1",
    tags=["base"]
)

@router.get("/", summary="Root Endpoint")
async def root():
    return {"message": "Welcome to the FastAPI application!"}

@router.get("/health", summary="Health Check Endpoint")
async def health_check(settings: Settings = Depends(get_settings)):
    """Endpoint to check the health of the API."""
    return {"status": "healthy", 
            "message": f"API is running - {settings.app_name} v{settings.app_version}"}