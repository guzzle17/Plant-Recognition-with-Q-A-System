"""
FastAPI application factory.

This module creates and configures the FastAPI application instance
with all necessary middleware, error handlers, and routers.
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import get_settings
from app.core.logging import setup_logging, get_logger
from app.core.exceptions import PlantBotException

# Initialize logging first
setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.

    Handles startup and shutdown events.
    """
    # Startup
    logger.info("Starting PlantBot API...")
    settings = get_settings()
    logger.info(f"Environment: {settings.app_env}")
    logger.info(f"Model: {settings.bedrock_model_id}")
    yield
    # Shutdown
    logger.info("Shutting down PlantBot API...")


def create_app() -> FastAPI:
    """
    Application factory pattern for creating FastAPI app instance.

    Returns:
        Configured FastAPI application
    """
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        description="AI-powered plant care assistant using AWS Bedrock and Claude",
        version=settings.app_version,
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register custom exception handler
    @app.exception_handler(PlantBotException)
    async def plantbot_exception_handler(request: Request, exc: PlantBotException):
        """Handle custom PlantBot exceptions."""
        logger.error(f"PlantBot exception: {exc.message}", extra={"details": exc.details})
        return JSONResponse(
            status_code=500,
            content={
                "error": exc.message,
                "details": exc.details
            }
        )

    # Register global exception handler
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        """Handle unexpected exceptions."""
        logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal server error",
                "message": "An unexpected error occurred"
            }
        )

    # Register API routers
    from app.api.v1 import router as v1_router
    app.include_router(v1_router.router, prefix="/api/v1")

    logger.info("FastAPI app created successfully")
    return app



