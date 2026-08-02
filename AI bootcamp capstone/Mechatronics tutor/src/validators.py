"""!
@file validators.py
@brief Input validation for troubleshooting requests.
"""

from __future__ import annotations
from src.models import TroubleshootingRequest


## @brief Validate required fields and practical input limits.
## @param request The request submitted by the user.
## @return A list of human-readable errors; an empty list means valid.
def validate_request(request: TroubleshootingRequest) -> list[str]:
    errors: list[str] = []
    if not request.symptom.strip():
        errors.append("Please describe the main symptom.")
    elif len(request.symptom.strip()) < 10:
        errors.append(
            "The symptom is too short. Include what the system does and what you expected."
        )
    combined_length = sum(
        len(value)
        for value in (
            request.symptom,
            request.observations,
            request.recent_changes,
            request.constraints,
        )
    )
    if combined_length > 8000:
        errors.append("Keep the combined fault description below 8,000 characters.")
    return errors
