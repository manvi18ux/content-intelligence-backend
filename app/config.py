# =============================================================================
# Application Configuration
# =============================================================================
# Centralized settings management using pydantic-settings.
#
# How it works:
#   1. Reads from .env file (if present)
#   2. Environment variables override .env values
#   3. Defaults are used if neither .env nor env var is set
#
# Usage:
#   from app.config import settings
#   print(settings.OPENAI_API_KEY)
# =============================================================================

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    Pydantic-settings automatically:
      - Reads .env file from the project root
      - Validates types (e.g., PORT must be an int)
      - Raises clear errors if required vars are missing
    """

    # -------------------------------------------------------------------------
    # OpenAI Configuration
    # -------------------------------------------------------------------------
    OPENAI_API_KEY: str = ""  # Empty default = graceful degradation in dev
    OPENAI_MODEL: str = "gpt-4o-mini"

    # -------------------------------------------------------------------------
    # Server Configuration
    # -------------------------------------------------------------------------
    PORT: int = 8000
    HOST: str = "0.0.0.0"

    # -------------------------------------------------------------------------
    # Application Settings
    # -------------------------------------------------------------------------
    LOG_LEVEL: str = "INFO"
    MAX_PIPELINE_ITERATIONS: int = 2
    APP_ENV: str = "development"

    # -------------------------------------------------------------------------
    # Pydantic-settings Configuration
    # -------------------------------------------------------------------------
    model_config = SettingsConfigDict(
        env_file=".env",           # Load from .env file in project root
        env_file_encoding="utf-8",
        case_sensitive=True,       # ENV vars are case-sensitive
        extra="ignore",            # Ignore unknown env vars silently
    )

    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.APP_ENV == "development"

    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return self.APP_ENV == "production"

    @property
    def has_openai_key(self) -> bool:
        """Check if a valid OpenAI API key is configured."""
        return bool(self.OPENAI_API_KEY and self.OPENAI_API_KEY != "sk-your-api-key-here")


# ---------------------------------------------------------------------------
# Singleton instance — import this throughout the application
# ---------------------------------------------------------------------------
settings = Settings()
