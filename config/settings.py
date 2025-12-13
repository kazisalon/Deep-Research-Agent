"""Application settings and configuration management."""

from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""
    
    # API Keys
    tavily_api_key: str
    google_api_key: str = ""  # Make optional since we're using Groq now
    groq_api_key: str = ""  # Groq API key for LLM
    
    # Model Configuration
    model_name: str = "gemini-1.5-flash"
    model_temperature: float = 0.0
    max_search_results: int = 3
    
    # Agent Configuration
    max_search_attempts: int = 3
    enable_caching: bool = True
    log_level: str = "INFO"
    
    # Cost Tracking
    track_costs: bool = True
    cost_per_search: float = 0.001
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    def validate_keys(self) -> bool:
        """Validate that required API keys are set."""
        if "your_" in self.tavily_api_key.lower():
            raise ValueError(
                "TAVILY_API_KEY not set. Please update your .env file."
            )
        if "your_" in self.google_api_key.lower():
            raise ValueError(
                "GOOGLE_API_KEY not set. Please update your .env file."
            )
        return True


# Global settings instance
settings = Settings()
