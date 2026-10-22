#!/usr/bin/env python3
"""Offline text comparison; not source-identity or legal-proposition validation."""

import argparse
from collections import Counter
import json
from pathlib import Path
import re
import sys
import unicodedata


MAX_MANIFEST_BYTES = 1_000_000
MAX_SOURCE_BYTES = 10_000_000
TYPOGRAPHY = str.maketrans({"‘": "'", "’": "'", "“": '"', "”": '"', "–": "-", "—": "-"})
ELLIPSIS = re.compile(r"\u2026|\.(?:\s*\.){2,3}")
LIMIT = ("Text comparison only. Source identity, omission context, legal support, "
         "precedential weight and subsequent treatment require separate review.")


def normalized(text):
    """Preserve words, numbers, case and punctuation other than listed typography."""
    return re.sub(r"\s+", " ", unicodedata.normalize("NFC", text).translate(TYPOGRAPHY)).strip()


def find_text(source, quote, offset=0):
    prefix = r"(?<!\w)" if re.match(r"\w", quote[0]) else ""
    suffix = r"(?!\w)" if re.match(r"\w", quote[-1]) else ""
    return re.compile(prefix + re.escape(quote) + suffix).search(source, offset)


def compare_quote(quote, source):
    if not isinstance(quote, str) or not quote.strip():
        raise ValueError("Quotation text must be a nonempty string")
    if "[" in quote or "]" in quote:
        return {"status": "manual_review", "reason": "Bracketed text or alteration requires comparison in context"}
    # Inspect omissions before a literal match: even a source containing the same
    # ellipsis does not establish that the draft's omission is legally accurate.
    if ELLIPSIS.search(quote):
        segments = [normalized(part) for part in ELLIPSIS.split(quote) if normalized(part)]
        if not segments:
            return {"status": "manual_review", "reason": "No substantive text between omission markers"}
        haystack = normalized(source)
        offset = 0
        for segment in segments:
            match = find_text(haystack, segment, offset)
            if match is None:
                return {"status": "not_found", "reason": "Omission segments do not all occur in order in this source"}
            offset = match.end()
        return {"status": "segmented_review", "reason": "Segments occur in order; review omitted material and attribution"}
    if find_text(source, quote):
        return {"status": "exact", "reason": "Literal text occurs in the supplied source"}
    if find_text(normalized(source), normalized(quote)):
        return {"status": "normalized", "reason": "Text occurs after NFC, listed typography and whitespace normalization"}
    return {"status": "not_found", "reason": "No literal or permitted normalized match in the cited source"}


def read_bounded(path, limit):
    with path.open("rb") as stream:
        data = stream.read(limit + 1)
    if len(data) > limit:
        raise ValueError(f"Input exceeds {limit} bytes: {path.name}")
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ValueError(f"Input is not UTF-8 text: {path.name}") from error


def source_path(root, value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Each authority needs a relative file path")
    path = Path(value)
    if path.is_absolute() or ".." in path.parts or not path.parts:
        raise ValueError("Source paths must remain relative to the manifest directory")
    candidate = root / path
    for item in (candidate, *candidate.parents):
        if item == root:
            break
        if item.is_symlink():
            raise ValueError("Source symlinks are not accepted")
    if not candidate.resolve().is_relative_to(root):
        raise ValueError("Source path escapes the manifest directory")
    return candidate


def indexed(records, label):
    if not isinstance(records, list):
        raise ValueError(f"{label} must be an array")
    result = {}
    for record in records:
        if not isinstance(record, dict):
            raise ValueError(f"Each {label} entry must be an object")
        identifier = record.get("id")
        if not isinstance(identifier, str) or not identifier.strip() or identifier in result:
            raise ValueError(f"Each {label} entry needs a unique, nonempty string id")
        result[identifier] = record
    return result


def audit_manifest(manifest):
    manifest = Path(manifest).resolve()
    try:
        payload = json.loads(read_bounded(manifest, MAX_MANIFEST_BYTES))
    except json.JSONDecodeError as error:
        raise ValueError("Manifest is not valid JSON") from error
    if not isinstance(payload, dict):
        raise ValueError("Manifest must be an object")
    authorities = indexed(payload.get("authorities"), "authorities")
    quotations = indexed(payload.get("quotations"), "quotations")
    if not quotations:
        raise ValueError("At least one quotation is required")
    sources = {}
    for identifier, record in authorities.items():
        path = source_path(manifest.parent, record.get("file"))
        if path.exists() and not path.is_file():
            raise ValueError("Authority file must be a regular text file")
        sources[identifier] = read_bounded(path, MAX_SOURCE_BYTES) if path.is_file() else None
    results = []
    for identifier, record in quotations.items():
        authority_id = record.get("authority_id")
        if not isinstance(authority_id, str) or authority_id not in authorities:
            raise ValueError(f"Quotation {identifier} references an unknown authority")
        quote = record.get("text")
        if not isinstance(quote, str) or not quote.strip():
            raise ValueError(f"Quotation {identifier} has no text")
        source = sources[authority_id]
        finding = ({"status": "missing_source", "reason": "The explicitly listed source file is absent"}
                   if source is None else compare_quote(quote, source))
        results.append({"id": identifier, "authority_id": authority_id, **finding})
    return {"scope": LIMIT, "counts": dict(Counter(r["status"] for r in results)), "results": results}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path, help="JSON manifest listing local UTF-8 sources and quotations")
    args = parser.parse_args(argv)
    try:
        report = audit_manifest(args.manifest)
    except (OSError, ValueError) as error:
        print(f"Invalid input: {error}", file=sys.stderr)
        return 2
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return int(any(row["status"] not in {"exact", "normalized"} for row in report["results"]))


if __name__ == "__main__":
    raise SystemExit(main())
