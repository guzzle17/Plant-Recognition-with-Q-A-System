"""
Configuration management for the PlantBot application.

Uses Pydantic Settings to load and validate configuration from environment variables.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from typing import List


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """

    # Application Settings
    app_name: str = "PlantBot API"
    app_version: str = "1.0.0"
    app_env: str = "development"
    log_level: str = "INFO"

    # AWS Configuration
    aws_region: str
    aws_access_key_id: str
    aws_secret_access_key: str

    # Bedrock Configuration
    bedrock_model_id: str = "anthropic.claude-3-haiku-20240307-v1:0"
    bedrock_max_tokens: int = 3000
    bedrock_temperature: float = 0.7
    bedrock_top_p: float = 0.9

    # API Configuration
    cors_origins: str = "http://localhost:3000"
    max_message_length: int = 1000

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.cors_origins.split(",")]

    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.app_env.lower() == "production"


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.

    Returns:
        Settings instance with loaded configuration
    """
    return Settings()

