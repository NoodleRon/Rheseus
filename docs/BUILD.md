# Rheseus 0.1.0 — build and evaluation record

22 October 2026.

## Objective and boundary

Create a working fork of Mike Workflows named **Rheseus**, add reusable methods
for supported legal analysis and concise resolutions, and keep local use separate
from deployment. Preserve the upstream history and notices. Publish only generic
methods, development material and explicitly fictional examples.

This is the workflow library, not a fork or deployment of the full Mike web
application. No client record, private matter link, executed agreement, actual
deal term, credential or opinion downloaded for a private matter is part of the
release.

## Plan and implementation

1. **Establish the source and repository conventions.** Start from upstream
   revision `20bed204ce9ef07e1bc2df0b16b35ee8ad997fb1`; inspect the README,
   contribution/versioning/provenance rules, schemas and existing validation.
2. **Preserve compatibility.** Leave inherited workflow identifiers and content
   intact. Add four assistant workflows and one tabular workflow as separately
   versioned add-on packs under the existing collection structure.
3. **Implement the review methods.** Add source-bounded matter review; concise
   factor/resolution and email drafting; cross-document contract review; and
   free-source authority verification. Keep existing facts, proposed terms,
   assumptions and legal requirements distinct.
4. **Address tabular execution behavior.** Place relevant source/status
   constraints in every consumed column prompt, because Mike's own tabular
   runner does not currently use the Markdown instruction body. Keep the
   canonical generated instructions synchronized for other consumers.
5. **Implement bounded quotation comparison.** Add an offline, standard-library
   Python utility using an explicit source manifest. Preserve words, numbers,
   case and negation; distinguish text matching from source authenticity and
   legal support. Mark omissions and bracketed alterations for review.
6. **Document and validate.** Add review and quotation guides, provenance,
   development requirements, a fictional example, schema-instance validation
   and quotation regression tests. Extend the inherited CI workflow.
7. **Publish the verified fork.** Inspect the diff and file set, commit the
   changes, push to the fork and verify the remote commit. This does not deploy
   a service or globally install skills.

## Design evaluation

The separate-pack approach makes additions discoverable without rewriting the
upstream catalog. Relative documentation and tool links assume that the repository
layout is retained. Copying only a skill folder will omit shared resources;
runtime-specific packaging needs a compatible import mechanism and has not been
certified here.

The concise workflow changes the upstream issues-list presentation to match a
brief/email request while retaining the material current position and concrete
resolution. The contract workflow keeps the coverage ledger and cross-document
reasoning but does not adopt a generic house form as proof of appropriate terms.
The regulated-services lens asks fact-sensitive questions rather than embedding
a state whitelist or a compliance conclusion.

The authority audit is independent of paid database access. Its checks are
explicitly separate: source identity, text, proposition support, authority weight
and subsequent treatment. Free-source access limits remain visible. The utility
does not provide a citator, legal interpretation, retrieval or OCR.

## Verification scope

Repository checks cover metadata, identifiers, manifests, column schemas,
canonical instructions, declared document assets and relative resource links.
Skill validation checks frontmatter and unfinished scaffolding. These establish
structural consistency, not that a model will follow the instructions correctly.

Quotation tests exercise literal and typographical matches, preserved negation,
amounts and case, word boundaries, Unicode composition, ellipsis order, bracketed
changes, missing sources, invalid inputs, path containment, symlink rejection,
size/encoding limits, identifier integrity, CLI exit codes and unchanged source
files. The fictional example exercises the command-line path end to end.

No live Mike import, LLM behavioral benchmark, external API integration,
confidential-document trial or deployment is claimed. A source match alone
cannot establish that a quotation is correctly attributed or legally applicable.

## Completed local checks

- Upstream repository validation: **174 workflows, 29 column files and 12 packs**.
- JSON Schema validation: **3 schema documents and 215 instances**.
- Tests: **19 quotation tests and 7 inherited helper tests passed**.
- Skill-creator validation: **all 5 new Rheseus skills passed**.
- Generation: **all 29 tabular skill bodies were stable after regeneration**.
- Resources: **19 relative links in new documentation and skills resolved**.
- Demonstration: **one exact and one permitted normalized match**, exit code 0.
- Diff checks: no whitespace errors; selected publication paths contain the new
  methods and fictional example, without client identifiers or local matter paths.

These checks were run before publication. They do not expand the verification
scope described above or substitute for testing a chosen runtime on real tasks.
