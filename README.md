# Rheseus

Portable legal workflows for source-supported review, concrete resolutions and
concise writing. Version **0.1.0**.

Rheseus is a fork of [Mike Workflows](https://github.com/open-legal-products/mike-workflows).
It adds two separately named packs while retaining the upstream workflows,
history and license notices. It is a workflow library with an optional offline
text-comparison utility. It does not deploy the Mike application or a legal
database. See [upstream documentation](UPSTREAM.md).

## Workflows

| Workflow | Use |
| --- | --- |
| [Matter Review](assistant-workflows/rheseus-pack/rheseus-matter-review/SKILL.md) | Analyze a supplied matter, reconcile competing proposals and recommend a supported resolution. |
| [Factor Resolution](assistant-workflows/rheseus-pack/rheseus-factor-resolution/SKILL.md) | Produce punchy factor → resolution bullets and a short email without losing material conditions. |
| [Contract Review](assistant-workflows/rheseus-pack/rheseus-contract-review/SKILL.md) | Review the complete available contract package, propose language and fallbacks, and identify evidence dependencies. |
| [Free Authority Audit](assistant-workflows/rheseus-pack/rheseus-free-authority-audit/SKILL.md) | Check source identity, quotations, proposition support, authority weight and the scope of subsequent-treatment research. |
| [Evidence Review](tabular-review-workflows/rheseus-pack/rheseus-evidence-review/SKILL.md) | Extract document-level terms and gaps into a source-anchored matrix. |

The assistant and tabular packs have separate manifests under their respective
collections. Existing upstream identifiers and defaults are unchanged.

## Use locally

Keep the repository layout intact so that workflow links to shared documentation
and optional tools resolve. Give a compatible assistant the selected workflow
file and explicitly identify the documents and research sources it may use.
These files do not authorize discovery of additional local client material.
See the [review standard](docs/REVIEW_STANDARD.md).

Within Mike, tabular runs currently consume `table-columns.yaml` with system
prompts rather than the tabular skill's Markdown body. The Rheseus columns
therefore carry the relevant source restrictions and evidence-status rules
themselves. Retain the column file with the skill. Runtime import and execution
in Mike or another assistant have not been tested in this release; metadata and
repository compatibility have been validated.

The skills are provider-neutral. No API key or paid subscription is required to
read them or run the offline utility. Research access and model execution depend
on the chosen environment. Free-source preferences do not imply unlimited API
access, complete coverage or comprehensive citator capability.

## Offline quotation check

Python 3.10+ is sufficient for the utility and its tests:

```sh
python3 tools/verify_quotations.py examples/quotations/manifest.json
python3 -m unittest discover -s tests -p 'test_*.py'
```

The committed example is fictional. The utility compares only explicitly listed
UTF-8 text files, makes no network calls and does not modify its inputs. A match
does not establish source authenticity, legal support or current validity.
See [inputs, normalization and result meanings](docs/QUOTATION_TOOL.md).

## Development and validation

For isolated development dependencies and repository-wide checks:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python workflow-schema/validate-workflows.py
.venv/bin/python tools/validate_schemas.py
.venv/bin/python -m unittest discover -s workflow-schema -p 'test_*.py'
.venv/bin/python -m unittest discover -s tests -p 'test_*.py'
```

The upstream tabular generator remains available. If changing its canonical
instruction block, regenerate the skills and inspect the resulting diff as
described in [UPSTREAM.md](UPSTREAM.md). CI checks generated consistency,
metadata, schema documents, columns, manifests and tests.

## Scope and provenance

The new workflows contain methods, not client facts or jurisdiction-specific
compliance approvals. The contract workflow includes a regulated-services lens,
but actual rules must be researched for the chosen jurisdiction, date and facts.

Rheseus additions are MIT licensed; upstream and more specific third-party
notices remain applicable. See [LICENSE](LICENSE), [upstream provenance policy](PROVENANCE.md),
[Rheseus provenance](docs/RHESEUS_PROVENANCE.md) and the [build/evaluation record](docs/BUILD.md).
No deployment, global skill installation or external matter upload is part of
this release.
