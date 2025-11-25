"""
Health check models.

Pydantic models for health check endpoint responses.
"""

from pydantic import BaseModel, Field
from typing import Dict, Any


class HealthResponse(BaseModel):
    """Response model for health check endpoint."""

    status: str = Field(
        ...,
        description="Health status of the API",
        examples=["healthy"]
    )

    version: str = Field(
        ...,
        description="API version",
        examples=["1.0.0"]
    )

    environment: str = Field(
        ...,
        description="Current environment",
        examples=["development", "production"]
    )

    services: Dict[str, str] = Field(
        default_factory=dict,
        description="Status of dependent services"
    )

