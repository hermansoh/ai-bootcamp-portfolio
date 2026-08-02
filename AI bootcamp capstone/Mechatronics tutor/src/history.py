"""!
@file history.py
@brief In-memory session history and JSON export helpers.
"""

from __future__ import annotations
import json
from datetime import datetime, timezone
from src.models import TroubleshootingRequest


## @brief Add one completed request and response to session history.
## @param history Mutable list held in Streamlit session state.
## @param request Structured user request.
## @param response AI-generated troubleshooting plan.
def add_history_record(
    history: list[dict],
    request: TroubleshootingRequest,
    response: str,
) -> None:
    history.append(
        {
            "created_at": datetime.now(timezone.utc).isoformat(),
            "request": request.to_dict(),
            "response": response,
        }
    )


## @brief Serialise session history for the download button.
## @param history Session records to export.
## @return UTF-8 JSON text.
def export_history_json(history: list[dict]) -> str:
    return json.dumps(history, indent=2, ensure_ascii=False)
