"""
Pydantic models for chat endpoints.

These models define the request and response schemas for the chat API,
including validation rules and documentation.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""

    message: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="User message to send to the AI",
        examples=["How do I care for a succulent?"]
    )

    stream: bool = Field(
        default=False,
        description="Whether to stream the response"
    )

    @field_validator("message")
    @classmethod
    def validate_message(cls, v: str) -> str:
        """Validate and clean the message."""
        # Strip whitespace
        v = v.strip()

        # Check if empty after stripping
        if not v:
            raise ValueError("Message cannot be empty or only whitespace")

        return v


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""

    reply: str = Field(
        ...,
        description="AI-generated response"
    )

    model: Optional[str] = Field(
        default=None,
        description="Model ID used for generation"
    )


class StreamChunk(BaseModel):
    """Model for streaming response chunks."""

    chunk: str = Field(
        ...,
        description="Text chunk from streaming response"
    )

