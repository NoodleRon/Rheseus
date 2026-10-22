# Offline quotation comparison

`tools/verify_quotations.py` uses Python 3.10+ and the standard library. It makes
no network requests and reads only sources explicitly listed in a JSON manifest.
Prepare UTF-8 text copies of the actual authorized sources first. A PDF, HTML
page, OCR transcript or opinion must be extracted and checked separately; this
tool neither performs extraction nor establishes authenticity.

## Input

Save a manifest beside its source text files, or above them in the same directory
tree. This example is fictional, not a case citation:

```json
{
  "authorities": [{"id": "example", "file": "source.txt"}],
  "quotations": [
    {"id": "q1", "authority_id": "example", "text": "The owner may not assign."}
  ]
}
```

Run the committed fictional demonstration from the repository root:

```sh
python3 tools/verify_quotations.py examples/quotations/manifest.json
```

JSON results go to standard output. The utility does not write or modify files.
For real work, pass the actual authorized manifest's path instead of the example.
Manifest paths may be absolute, but source paths within a manifest must be
relative and remain inside its directory tree. Source symlinks are rejected.
The manifest limit is 1 MB; each source limit is 10 MB. Duplicate identifiers,
unknown authority references, non-UTF-8 sources and malformed inputs are errors.

## Results and interpretation

| Result | Meaning |
| --- | --- |
| `exact` | The literal text occurs in the supplied cited source. |
| `normalized` | A match follows Unicode NFC, curly-quote/dash substitution and whitespace normalization. Words, case and numbers are preserved. Inspect formatting and context. |
| `segmented_review` | Ellipsis-separated segments occur in order. Check the omission and surrounding context. |
| `manual_review` | Bracketed text or an omission without substantive text needs review. |
| `not_found` | No permitted match was found in the cited source. This is not a finding of fabrication. |
| `missing_source` | The explicitly listed file is absent. Retrieval is unresolved. |

Exit code **0** means every quotation had an exact or permitted normalized text
match; **1** means at least one result needs review; **2** means invalid or unreadable
input. No code means that the legal analysis passed. No fuzzy threshold can turn
changed words, amounts or negation into a match. The utility does not search
other sources for attribution errors; the reviewer must investigate them.

The tool does not verify source identity, page pinpoints, OCR reliability, speaker
attribution, holdings, binding weight, amendments or subsequent treatment. Text
can match while being misleadingly attributed or legally inapplicable. Use the
authority-audit workflow for those judgments.
