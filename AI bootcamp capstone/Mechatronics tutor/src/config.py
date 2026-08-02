"""!
@file config.py
@brief Environment-based configuration for MechaMentor.
"""

from __future__ import annotations
import os
from dataclasses import dataclass
from dotenv import load_dotenv


class ConfigurationError(RuntimeError):
    """Raised when a required application setting is missing."""


@dataclass(frozen=True)
class AppConfig:
    """Application settings loaded from environment variables."""

    groq_api_key: str
    groq_model: str
    temperature: float = 0.2
    max_tokens: int = 1400

    ## @brief Load and validate configuration from environment variables.
    ## @return A validated AppConfig instance.
    ## @raises ConfigurationError If GROQ_API_KEY or GROQ_MODEL is missing.
    @classmethod
    def from_environment(cls) -> "AppConfig":
        load_dotenv()
        api_key = os.getenv("GROQ_API_KEY", "").strip()
        model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant").strip()
        if not api_key:
            raise ConfigurationError(
                "GROQ_API_KEY is missing. Copy .env.example to .env and add your key."
            )
        if not model:
            raise ConfigurationError("GROQ_MODEL is blank. Add a valid Groq model ID.")
        return cls(groq_api_key=api_key, groq_model=model)
