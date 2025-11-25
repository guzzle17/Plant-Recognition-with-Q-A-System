"""
Custom exceptions for the PlantBot application.

This module defines custom exception classes that provide more specific
error handling throughout the application.
"""


class PlantBotException(Exception):
    """Base exception for all PlantBot errors."""
    def __init__(self, message: str, details: dict = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


class BedrockServiceError(PlantBotException):
    """Raised when there's an error communicating with AWS Bedrock."""
    pass


class ModelInvocationError(PlantBotException):
    """Raised when model invocation fails."""
    pass


class ConfigurationError(PlantBotException):
    """Raised when there's a configuration issue."""
    pass


class ValidationError(PlantBotException):
    """Raised when input validation fails."""
    pass

