"""
Chat service for orchestrating plant-related conversations.

This service uses langchain_aws ChatBedrockConverse directly for AI interactions.
"""

from typing import Iterator
from functools import lru_cache
import boto3

from langchain_aws import ChatBedrock
from langchain_core.messages import HumanMessage, SystemMessage

from app.core.config import get_settings
from app.core.logging import get_logger
from app.core.prompts import get_system_prompt
from app.core.exceptions import ModelInvocationError

logger = get_logger(__name__)


class ChatService:
    """
    Service for handling chat interactions with the PlantBot AI.

    Uses AWS Bedrock via LangChain for AI-powered plant care assistance.
    This layer can be extended to add features like:
    - Conversation history management
    - Context injection
    - Response filtering
    - Usage tracking
    """

    def __init__(self):
        """Initialize chat service with AWS Bedrock LLM."""
        settings = get_settings()

        try:
            # Initialize ChatBedrock from langchain_aws
            # It will automatically use AWS credentials from environment variables or boto3 default session
            self.llm = ChatBedrock(
                model_id=settings.bedrock_model_id,
                region_name=settings.aws_region,
                credentials_profile_name=None,  # Use environment variables
                model_kwargs={
                    "temperature": settings.bedrock_temperature,
                    "top_p": settings.bedrock_top_p,
                    "max_tokens": settings.bedrock_max_tokens
                }
            )

            # Set system prompt for plant expert context
            self.system_message = SystemMessage(content=get_system_prompt())

            logger.info(f"ChatService initialized with model: {settings.bedrock_model_id}")

        except Exception as e:
            logger.error(f"Failed to initialize ChatService: {str(e)}")
            raise ModelInvocationError(
                "Failed to initialize AI service",
                details={"error": str(e)}
            )

    def generate_response(self, message: str) -> str:
        """
        Generate a response to a user message.

        Args:
            message: User's message

        Returns:
            AI-generated response

        Raises:
            ModelInvocationError: If AI invocation fails
        """
        logger.info(f"Generating response for message: {message[:50]}...")

        try:
            # Create message list with system prompt and user message
            messages = [
                self.system_message,
                HumanMessage(content=message)
            ]

            # Invoke the model
            response = self.llm.invoke(messages)

            logger.info("Response generated successfully")
            return response.content

        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            raise ModelInvocationError(
                "Failed to generate AI response",
                details={"error": str(e), "message": message[:50]}
            )

    def generate_streaming_response(self, message: str) -> Iterator[str]:
        """
        Generate a streaming response to a user message.

        Args:
            message: User's message

        Yields:
            Chunks of the AI-generated response

        Raises:
            ModelInvocationError: If AI invocation fails
        """
        logger.info(f"Generating streaming response for message: {message[:50]}...")

        try:
            # Create message list with system prompt and user message
            messages = [
                self.system_message,
                HumanMessage(content=message)
            ]

            # Stream the response
            for chunk in self.llm.stream(messages):
                if hasattr(chunk, 'content') and chunk.content:
                    yield chunk.content

            logger.info("Streaming response completed")

        except Exception as e:
            logger.error(f"Error streaming response: {str(e)}")
            raise ModelInvocationError(
                "Failed to stream AI response",
                details={"error": str(e), "message": message[:50]}
            )


@lru_cache()
def get_chat_service() -> ChatService:
    """
    Get a cached chat service instance.

    Returns:
        Singleton ChatService instance
    """
    return ChatService()

