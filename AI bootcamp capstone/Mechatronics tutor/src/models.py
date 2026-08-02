"""!
@file models.py
@brief Data models used by the troubleshooting pipeline.
"""

from __future__ import annotations
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class TroubleshootingRequest:
    """Structured information supplied by the user."""

    system_type: str
    symptom: str
    observations: str
    recent_changes: str
    constraints: str
    experience_level: str

    ## @brief Convert the request into a serialisable dictionary.
    ## @return Dictionary containing every request field.
    def to_dict(self) -> dict[str, str]:
        return asdict(self)
