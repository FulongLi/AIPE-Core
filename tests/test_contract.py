import copy
import json
from pathlib import Path
import socket
import tempfile
import unittest
from unittest.mock import patch

from scripts.validate import ROOT, load_json, state_validator, validate_state


class EngineeringStateTests(unittest.TestCase):
    def setUp(self):
        self.state = load_json(ROOT / "examples/dab-10kw/engineering-state.json")

    def assertInvalid(self, text=None):
        errors = validate_state(self.state)
        self.assertTrue(errors)
        if text:
            self.assertTrue(any(text in error for error in errors), errors)

    def test_example_passes_with_network_disabled(self):
        with patch.object(socket, "socket", side_effect=AssertionError("network forbidden")):
            self.assertEqual(validate_state(self.state), [])

    def test_schema_documents_are_valid(self):
        self.assertIsNotNone(state_validator())

    def test_missing_top_level_domain_is_rejected(self):
        del self.state["thermal"]
        self.assertInvalid("required property")

    def test_unknown_top_level_and_domain_fields_are_rejected(self):
        for obj in [self.state, self.state["requirements"], self.state["project"]]:
            with self.subTest(obj=obj):
                obj["typo"] = 1
                self.assertInvalid("Additional properties")
                del obj["typo"]

    def test_quantity_requires_explicit_si_units(self):
        self.state["requirements"]["nominal_power"] = 10000
        self.assertInvalid("object")
        self.state["requirements"]["nominal_power"] = {"value": 10, "unit": "kW"}
        self.assertInvalid("W")

    def test_wrong_physical_dimension_is_rejected(self):
        self.state["requirements"]["input_voltage"]["unit"] = "W"
        self.assertInvalid("V")

    def test_negative_frequency_is_rejected(self):
        self.state["requirements"]["switching_frequency"]["value"] = -1
        self.assertInvalid()

    def test_non_finite_host_values_are_rejected(self):
        self.state["requirements"]["nominal_power"]["value"] = float("inf")
        self.assertInvalid("finite")

    def test_invalid_date_and_version_are_rejected(self):
        self.state["project"]["created_at"] = "2026-99-99"
        self.assertInvalid("date-time")
        self.state["schema_version"] = "1.0.0"
        self.assertInvalid("0.1.0")

    def test_namespaced_extensions_are_allowed(self):
        self.state["extensions"] = {"example.custom": {"independent_domain": 3}}
        self.assertEqual(validate_state(self.state), [])
        self.state["extensions"] = {"typo": {}}
        self.assertInvalid()

    def test_missing_evidence_reference_is_rejected(self):
        self.state["requirements"]["evidence_refs"] = ["evidence.missing"]
        self.assertInvalid("unknown evidence")

    def test_quantities_need_evidence(self):
        self.state["requirements"]["evidence_refs"] = []
        self.assertInvalid("require evidence_refs")

    def test_duplicate_ids_are_rejected(self):
        self.state["evidence"].append(copy.deepcopy(self.state["evidence"][0]))
        self.assertInvalid("Duplicate entity id")

    def test_provenance_cycle_is_rejected(self):
        self.state["evidence"][0]["provenance"]["inputs"] = ["evidence.design-brief"]
        self.assertInvalid("Cyclic")

    def test_rejected_evidence_cannot_support_state(self):
        self.state["evidence"][0]["review_status"] = "rejected"
        self.assertInvalid("rejected evidence")

    def test_measurement_requires_artifact_and_tool(self):
        self.state["evidence"][0]["kind"] = "measurement"
        self.assertInvalid()

    def test_analytical_result_requires_inputs(self):
        self.state["evidence"][0]["kind"] = "analytical"
        self.assertInvalid()

    def test_cannot_promote_assumption_to_measured(self):
        self.state["validation"]["status"] = "measured"
        self.state["validation"]["checks"] = [{
            "id": "check.measurement", "kind": "measurement", "status": "pass",
            "description": "Unsupported measurement claim", "evidence_refs": ["evidence.design-brief"]}]
        self.assertInvalid("matching evidence")

    def test_validation_status_requires_corresponding_check(self):
        self.state["validation"]["status"] = "schema_validated"
        self.assertInvalid("passing schema check")

    def test_failed_check_cannot_have_successful_overall_status(self):
        self.state["validation"]["checks"] = [{"id": "check.failure", "kind": "schema",
            "status": "fail", "description": "Failure", "evidence_refs": []}]
        self.assertInvalid("Failed checks")

    def test_completed_simulation_needs_a_run(self):
        self.state["simulation"]["status"] = "completed"
        self.assertInvalid("matching run")

    def test_completed_run_requires_matching_evidence_and_operating_point(self):
        self.state["simulation"] = {"status": "completed", "evidence_refs": [], "runs": [{
            "id": "run.example", "status": "completed", "tool": {"id": "tool.example", "version": "1"},
            "model": {"uri": "example.json", "media_type": "application/json"},
            "outputs": [], "operating_point_ref": "operating-point.missing", "evidence_refs": []}]}
        self.assertInvalid("unknown operating point")
        self.assertInvalid("completed simulation requires")

    def test_json_loader_rejects_duplicate_keys_and_nonstandard_numbers(self):
        for content in ['{"id": 1, "id": 2}', '{"value": NaN}', '{"value": Infinity}']:
            with self.subTest(content=content), tempfile.TemporaryDirectory() as temp:
                path = Path(temp) / "invalid.json"
                path.write_text(content, encoding="utf-8")
                with self.assertRaises(ValueError):
                    load_json(path)


if __name__ == "__main__":
    unittest.main()
