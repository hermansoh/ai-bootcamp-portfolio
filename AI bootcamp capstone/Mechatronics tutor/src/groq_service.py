"""!
@file groq_service.py
@brief Groq API integration and response validation.
"""

from __future__ import annotations
from groq import APIConnectionError, APIStatusError, APITimeoutError, Groq, RateLimitError
from src.config import AppConfig


class AIServiceError(RuntimeError):
    """Raised when the AI provider cannot return a usable response."""


class GroqTroubleshootingService:
    """Small service wrapper around Groq Chat Completions."""

    ## @brief Construct the service using validated application configuration.
    ## @param config Groq API key, model ID, and generation parameters.
    def __init__(self, config: AppConfig) -> None:
        self._config = config
        self._client = Groq(api_key=config.groq_api_key)

    ## @brief Send the system and user prompts to Groq.
    ## @param system_prompt Named prompt defining the assistant's behaviour.
    ## @param user_prompt Structured fault information supplied by the user.
    ## @return A non-empty Markdown troubleshooting plan.
    ## @raises AIServiceError If the provider fails or returns an empty response.
    def generate_plan(self, system_prompt: str, user_prompt: str) -> str:
        try:
            completion = self._client.chat.completions.create(
                model=self._config.groq_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=self._config.temperature,
                max_tokens=self._config.max_tokens,
            )
        except RateLimitError as error:
            raise AIServiceError(
                "The Groq rate limit was reached. Wait briefly and try again."
            ) from error
        except APITimeoutError as error:
            raise AIServiceError(
                "The Groq request timed out. Check the connection and retry."
            ) from error
        except APIConnectionError as error:
            raise AIServiceError("The application could not connect to Groq.") from error
        except APIStatusError as error:
            raise AIServiceError(
                f"Groq returned API status {error.status_code}."
            ) from error
        except Exception as error:
            raise AIServiceError("An unexpected AI service error occurred.") from error

        if not completion.choices:
            raise AIServiceError("Groq returned no response choices.")
        content = completion.choices[0].message.content
        if not content or not content.strip():
            raise AIServiceError("Groq returned an empty response.")
        return content.strip()
