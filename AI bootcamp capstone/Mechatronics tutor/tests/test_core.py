"""Unit tests for deterministic MechaMentor helpers."""

from __future__ import annotations
import json
import unittest
from src.history import add_history_record, export_history_json
from src.models import TroubleshootingRequest
from src.prompting import build_user_prompt
from src.validators import validate_request


class CoreTests(unittest.TestCase):
    """Verify functions that do not require a live API key."""

    def make_request(self, symptom: str = "Motor stops when load is applied.") -> TroubleshootingRequest:
        return TroubleshootingRequest(
            system_type="Motor and drive system",
            symptom=symptom,
            observations="Driver fault LED turns on.",
            recent_changes="Mechanical load was increased.",
            constraints="Do not exceed 2 A during testing.",
            experience_level="Beginner",
        )

    def test_valid_request_has_no_errors(self) -> None:
        self.assertEqual(validate_request(self.make_request()), [])

    def test_blank_symptom_is_rejected(self) -> None:
        errors = validate_request(self.make_request(symptom=""))
        self.assertTrue(any("main symptom" in error for error in errors))

    def test_prompt_contains_user_evidence(self) -> None:
        prompt = build_user_prompt(self.make_request())
        self.assertIn("Motor stops when load is applied.", prompt)
        self.assertIn("Driver fault LED turns on.", prompt)

    def test_history_export_is_valid_json(self) -> None:
        history: list[dict] = []
        add_history_record(history, self.make_request(), "Test response")
        parsed = json.loads(export_history_json(history))
        self.assertEqual(parsed[0]["response"], "Test response")


if __name__ == "__main__":
    unittest.main()
