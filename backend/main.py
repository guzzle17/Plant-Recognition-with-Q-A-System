"""
PlantBot Backend - Main Application Entry Point

This is the main entry point for the FastAPI application.
The app uses the factory pattern defined in app/__init__.py
"""

from app import create_app

# Create the FastAPI application instance
app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
