"""
Shared dependencies for API endpoints.

This module provides dependency injection functions used across
multiple endpoints.
"""

from app.services.chat_service import ChatService, get_chat_service
from app.core.config import Settings, get_settings


def get_chat_service_dependency() -> ChatService:
    """
    Dependency for injecting ChatService.

    Returns:
        ChatService instance with AWS Bedrock LLM
    """
    return get_chat_service()


def get_settings_dependency() -> Settings:
    """
    Dependency for injecting Settings.

    Returns:
        Settings instance
    """
    return get_settings()

