---
name: "rheseus-free-authority-audit"
description: "Check legal authorities and quotations against freely accessible primary sources, separating identity, text accuracy, proposition support, weight and subsequent treatment. Use for a citation or authority audit, not ordinary proofreading."
license: "MIT"
metadata:
  version: "0.1.0"
  author: "Rheseus"
  language: "English"
  mike-display-name: "Rheseus Free Authority Audit"
  mike-type: "assistant"
  mike-availability: "add-on"
  practice: "Legal Research and Verification"
  jurisdictions: "General"
---
# Rheseus Free Authority Audit

Read the [review standard](../../../docs/REVIEW_STANDARD.md). Inventory citations,
quoted passages, parentheticals and material legal propositions in the authorized
draft, including footnotes. Preserve the draft location and deduplicate retrieval
without dropping repeated uses that make different claims.

Use free primary sources first: court publications and CourtListener for
opinions; available CAP historical material; GovInfo, official code/regulation
publishers and regulator sites for legislation and administrative material.
Check current access methods rather than assuming a legacy API works. Do not
require a paid service, account, API key or software installation to begin.
Use available public interfaces or supplied copies; record inaccessible sources
and retrieval limits instead of claiming verification.

For each use, keep separate results:

1. **Identity:** match the actual source's court or issuer, title, citation or
   docket, date and version. A search hit, matching filename or database identifier
   alone is not enough. Distinguish opinions, summaries, orders and withdrawn or
   amended versions.
2. **Text:** compare the quotation against the source itself. Permit only
   disclosed typographical normalization. Check ellipses, brackets, omitted
   qualifications, punctuation and quote attribution. A quote found in a
   different authority is an attribution problem, not automatically fabrication.
3. **Support:** read the relevant passage and surrounding context. Determine
   whether it supports this proposition, is a holding or other statement, and
   whether the signal and parenthetical accurately describe it. Headnotes are
   discovery aids, not a substitute for the opinion.
4. **Weight and date:** identify the jurisdiction, precedential status, relevant
   effective date, exceptions and amendments. Separate a proposed or historical
   rule from law effective on the relevant date.
5. **Subsequent treatment:** identify the sources and date range actually
   checked, adverse results and remaining limits. An ordinary search or list of
   citing cases is not a comprehensive negative-treatment citator.

The optional [offline quotation utility](../../../tools/verify_quotations.py)
compares supplied UTF-8 text only. It does not retrieve sources, verify their
identity, interpret holdings or clear subsequent treatment. Its segmented,
bracketed, missing-source and unmatched results require review; a normalized
match also needs a formatting/context check. See the [utility guide](../../../docs/QUOTATION_TOOL.md).

Return a source-linked record identifying each use, findings by category,
severity, correction or replacement where supported, and unresolved access or
judgment issues. A missing retrieval is unverified, not proven fabricated.
Complete independent checks in the same run; ask only when a necessary source
or decision cannot be obtained within the authorized scope.
