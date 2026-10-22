#!/usr/bin/env python3
"""Validate all workflow schemas and their actual repository instances."""

from pathlib import Path
import re
import sys

from jsonschema import Draft202012Validator
import yaml


ROOT = Path(__file__).resolve().parents[1]


def main():
    validators = {}
    for path in (ROOT / "workflow-schema").glob("*.schema.yaml"):
        schema = yaml.safe_load(path.read_text())
        Draft202012Validator.check_schema(schema)
        validators[path.name] = Draft202012Validator(schema)
    count = 0
    errors = []
    for collection in ("assistant-workflows", "tabular-review-workflows"):
        for path in sorted((ROOT / collection).rglob("*")):
            if not path.is_file():
                continue
            if path.name == "SKILL.md":
                match = re.match(r"\A---\n(.*?)\n---\n", path.read_text(), re.DOTALL)
                if not match:
                    errors.append(f"{path.relative_to(ROOT)}: missing frontmatter")
                    continue
                data = yaml.safe_load(match.group(1))
                schema_name = "workflow-metadata.schema.yaml"
            elif path.name in {"pack.yaml", "table-columns.yaml"}:
                data = yaml.safe_load(path.read_text())
                schema_name = "pack.schema.yaml" if path.name == "pack.yaml" else "table-columns.schema.yaml"
            else:
                continue
            count += 1
            for error in validators[schema_name].iter_errors(data):
                errors.append(f"{path.relative_to(ROOT)}: {error.message}")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"Validated {len(validators)} schemas and {count} instances.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
