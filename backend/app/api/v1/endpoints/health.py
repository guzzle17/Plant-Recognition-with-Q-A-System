"""
Health check endpoint.

Provides a simple endpoint to check if the API is running and healthy.
"""

from fastapi import APIRouter, Depends
from app.models.health import HealthResponse
from app.core.config import Settings, get_settings
from app.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check(settings: Settings = Depends(get_settings)) -> HealthResponse:
    """
    Health check endpoint.

    Returns basic information about the API's health status,
    version, and environment.

    Returns:
        HealthResponse with status information
    """
    logger.debug("Health check requested")

    return HealthResponse(
        status="healthy",
        version=settings.app_version,
        environment=settings.app_env,
        services={
            "bedrock": "available",
            "api": "running"
        }
    )

