"""
API v1 router aggregation.

This module aggregates all v1 endpoints into a single router.
"""

from fastapi import APIRouter
from app.api.v1.endpoints import chat, health

# Create v1 router
router = APIRouter()

# Include all endpoint routers
router.include_router(health.router)
router.include_router(chat.router)

