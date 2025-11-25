"""
Chat endpoints for PlantBot AI interactions.

Provides both standard and streaming chat endpoints for users to
interact with the PlantBot AI assistant.
"""

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from typing import Iterator

from app.models.chat import ChatRequest, ChatResponse
from app.services.chat_service import ChatService
from app.api.dependencies import get_chat_service_dependency
from app.core.logging import get_logger
from app.core.exceptions import (
    PlantBotException,
    ModelInvocationError
)
from app.core.config import get_settings

logger = get_logger(__name__)
router = APIRouter()


@router.post("/chat", tags=["Chat"])
async def chat(
    req: ChatRequest,
    chat_service: ChatService = Depends(get_chat_service_dependency)
):
    """
    Generate a response to a user's plant-related question.

    This endpoint accepts a text message and returns an AI-generated response
    from the PlantBot assistant. The assistant is specialized in plant care,
    identification, and gardening advice.

    Args:
        req: Chat request containing the user's message
        chat_service: Injected chat service

    Returns:
        ChatResponse with the AI's reply

    Raises:
        HTTPException: If the request fails or an error occurs
    """
    logger.info(f"Chat request received: {req.message[:50]}...")

    try:
        # Handle streaming if requested
        if req.stream:
            logger.info("Streaming response requested")
            return StreamingResponse(
                stream_chat_response(req.message, chat_service),
                media_type="text/event-stream"
            )

        # Generate standard response
        settings = get_settings()
        reply = chat_service.generate_response(req.message)

        logger.info("Chat response generated successfully")
        return ChatResponse(
            reply=reply,
            model=settings.bedrock_model_id
        )

    except ModelInvocationError as e:
        logger.error(f"Model invocation error: {e.message}", exc_info=True)
        raise HTTPException(
            status_code=503,
            detail={
                "error": "AI model unavailable",
                "message": "The AI service is temporarily unavailable. Please try again later.",
                "details": e.details
            }
        )

    except PlantBotException as e:
        logger.error(f"PlantBot error: {e.message}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Internal error",
                "message": str(e.message),
                "details": e.details
            }
        )

    except Exception as e:
        logger.error(f"Unexpected error in chat endpoint: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Internal server error",
                "message": "An unexpected error occurred. Please try again later."
            }
        )


def stream_chat_response(
    message: str,
    chat_service: ChatService
) -> Iterator[str]:
    """
    Stream chat response chunks in Server-Sent Events format.

    Args:
        message: User's message
        chat_service: Chat service instance

    Yields:
        SSE-formatted response chunks
    """
    try:
        for chunk in chat_service.generate_streaming_response(message):
            # Format as Server-Sent Event
            yield f"data: {chunk}\n\n"

        # Send completion signal
        yield "data: [DONE]\n\n"

    except Exception as e:
        logger.error(f"Error during streaming: {str(e)}", exc_info=True)
        error_message = f"data: [ERROR] {str(e)}\n\n"
        yield error_message


