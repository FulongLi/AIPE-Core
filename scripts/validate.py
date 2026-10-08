"""Offline structure and cross-reference checks for AIPE Engineering State v0.1.

This is a contract validator, not an engineering solver or physical validator.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource
from referencing.exceptions import NoSuchResource

ROOT = Path(__file__).resolve().parents[1]


def load_json(path: Path) -> Any:
    """Reject nonstandard numbers and duplicate keys instead of losing information."""
    def reject_constant(value: str) -> None:
        raise ValueError(f"Non-finite JSON number: {value}")

    def unique_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"Duplicate JSON key: {key}")
            result[key] = value
        return result

    return json.loads(path.read_text(encoding="utf-8"),
                      parse_constant=reject_constant, object_pairs_hook=unique_keys)


def _offline_only(uri: str) -> Resource:
    raise NoSuchResource(ref=uri)


def state_validator(schema_dir: Path | None = None) -> Draft202012Validator:
    """Map logical versioned schema IDs to disk. Never download a remote schema."""
    schema_dir = schema_dir or ROOT / "schemas"
    schemas = [load_json(path) for path in sorted(schema_dir.glob("*.schema.json"))]
    for schema in schemas:
        Draft202012Validator.check_schema(schema)
    registry = Registry(retrieve=_offline_only).with_resources(
        (schema["$id"], Resource.from_contents(schema)) for schema in schemas
    )
    state = next(schema for schema in schemas
                 if schema["$id"].endswith("/engineering-state.schema.json"))
    checker = FormatChecker()
    required_formats = {"date-time", "uri", "uri-reference"}
    if not required_formats.issubset(checker.checkers):
        raise ValueError("Install requirements-dev.txt: JSON Schema format validators are required")
    return Draft202012Validator(state, registry=registry, format_checker=checker)


def _walk(value: Any, path: str = "$"):
    yield path, value
    if isinstance(value, dict):
        for key, item in value.items():
            # Extension payloads belong to their namespace's independent contract.
            if key != "extensions":
                yield from _walk(item, f"{path}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from _walk(item, f"{path}[{index}]")


def validate_state(state: Any, schema_dir: Path | None = None) -> list[str]:
    validator = state_validator(schema_dir)
    errors = [f"{error.json_path}: {error.message}"
              for error in sorted(validator.iter_errors(state), key=lambda e: e.json_path)]
    if errors:
        return errors

    # JSON Schema treats some host-language infinities as numbers. Catch them too.
    def finite(value: Any, path: str = "$"):
        if isinstance(value, float) and not math.isfinite(value):
            errors.append(f"{path}: number must be finite")
        elif isinstance(value, dict):
            for key, item in value.items():
                finite(item, f"{path}.{key}")
        elif isinstance(value, list):
            for index, item in enumerate(value):
                finite(item, f"{path}[{index}]")
    finite(state)

    entities = [state, state["project"], state["converter"],
                *state["requirements"].get("operating_points", []),
                *state["requirements"].get("constraints", []),
                *state["semiconductors"], *state["magnetics"], *state["passives"],
                *state["simulation"]["runs"], *state["validation"]["checks"],
                *state["evidence"]]
    seen = set()
    for entity in entities:
        identifier = entity["id"]
        if identifier in seen:
            errors.append(f"Duplicate entity id: {identifier}")
        seen.add(identifier)
    evidence = {item["id"]: item for item in state["evidence"]}
    for path, value in _walk(state):
        if not isinstance(value, dict):
            continue
        references = value.get("evidence_refs", [])
        if path.endswith(".provenance"):
            references = value["inputs"]
        for reference in references:
            if reference not in evidence:
                errors.append(f"{path}: unknown evidence reference {reference}")
            elif evidence[reference]["review_status"] == "rejected":
                errors.append(f"{path}: rejected evidence {reference}")
        # At least the enclosing domain object must trace physical quantities.
        physical = any(isinstance(item, dict) and set(item) == {"value", "unit"}
                       for item in value.values())
        if physical and not references:
            # Semiconductor ratings inherit their component's evidence_refs.
            if not path.endswith(".ratings"):
                errors.append(f"{path}: physical quantities require evidence_refs")
    for index, component in enumerate(state["semiconductors"]):
        if component.get("ratings") and not component["evidence_refs"]:
            errors.append(f"$.semiconductors[{index}]: ratings require evidence_refs")

    visiting, visited = set(), set()
    def visit(identifier: str):
        if identifier in visiting:
            errors.append(f"Cyclic evidence provenance at {identifier}")
            return
        if identifier in visited or identifier not in evidence:
            return
        visiting.add(identifier)
        for dependency in evidence[identifier]["provenance"]["inputs"]:
            visit(dependency)
        visiting.remove(identifier)
        visited.add(identifier)
    for identifier in evidence:
        visit(identifier)

    def has_kind(references: list[str], kind: str) -> bool:
        return any(reference in evidence and evidence[reference]["kind"] == kind
                   for reference in references)

    validation = state["validation"]
    physical_kinds = {"analytical", "simulation", "measurement"}
    for check in validation["checks"]:
        if (check["status"] == "pass" and check["kind"] in physical_kinds
                and not has_kind(check["evidence_refs"], check["kind"])):
            errors.append(f"{check['id']}: passing {check['kind']} check needs matching evidence")
    required_kind = {"schema_validated": "schema", "analytically_checked": "analytical",
                     "simulated": "simulation", "measured": "measurement",
                     "reviewed": "review"}.get(validation["status"])
    if required_kind and not any(check["status"] == "pass" and check["kind"] == required_kind
                                 for check in validation["checks"]):
        errors.append(f"Validation status {validation['status']} needs a passing {required_kind} check")
    if any(check["status"] == "fail" for check in validation["checks"]) and validation["status"] != "failed":
        errors.append("Failed checks require overall validation status failed")

    operating_points = {point["id"] for point in state["requirements"].get("operating_points", [])}
    runs = state["simulation"]["runs"]
    for run in runs:
        if run.get("operating_point_ref") and run["operating_point_ref"] not in operating_points:
            errors.append(f"{run['id']}: unknown operating point {run['operating_point_ref']}")
        if run["status"] == "completed" and (not run["outputs"] or not has_kind(run["evidence_refs"], "simulation")):
            errors.append(f"{run['id']}: completed simulation requires outputs and simulation evidence")
    status = state["simulation"]["status"]
    if status == "not_run" and runs:
        errors.append("Simulation status not_run requires no runs")
    if status in {"completed", "failed", "configured"} and not any(run["status"] == status for run in runs):
        errors.append(f"Simulation status {status} requires a matching run")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("states", nargs="+", type=Path)
    args = parser.parse_args()
    failed = False
    for path in args.states:
        try:
            errors = validate_state(load_json(path))
        except (OSError, ValueError) as error:
            errors = [str(error)]
        if errors:
            failed = True
            print(f"FAIL {path}")
            for error in errors:
                print(f"  {error}")
        else:
            print(f"PASS {path} (structure and references; no physical validation)")
    return int(failed)


if __name__ == "__main__":
    raise SystemExit(main())
