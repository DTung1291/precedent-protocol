# Consensus protocol

## Decision-bearing fields

The leader may use natural-language reasoning, but contract code recognizes
only bounded fields: five lens verdicts, explicit precedent relations, and
short explanations. The final verdict and contestability are derived in code.

Validators independently fetch every evidence URL and verify its SHA-256. They
then audit the leader's canonical panel rather than generating a second panel.
Consensus accepts only when:

1. the proposed panel normalizes without repair and has `basis_status=OK`;
2. the validator independently obtains every exact evidence byte;
3. all five bounded audit checks are present once and well formed; and
4. every check passes: `EVIDENCE_SUPPORT`, `POLICY_APPLICATION`,
   `COUNTERARGUMENT_FAIRNESS`, `PRECEDENT_RELATIONS`, and
   `VERDICT_DERIVATION`.

This is deliberately stricter than checking JSON shape. A well-formed but
unsupported answer cannot pass merely because it uses an allowed enum.

## Five independent lenses

- `FACTS`: evidentiary support and contradictions.
- `POLICY`: application of the immutable natural-language standard.
- `ADVERSARIAL`: strongest countercase and missing information.
- `PRECEDENT`: consistency with the selected prior cases.
- `REMEDY`: fit between the record and available outcomes.

The five outputs form a small deliberative ensemble. Contract code calculates
the majority and contestability. No LLM can directly set either field.

The audit model cannot change the panel, verdict, or contestability. It can only
accept or reject each proof obligation. The contract ignores any claimed
top-level approval flag and derives audit support as the conjunction of all
five normalized checks. Protocol validators therefore compare a bounded
boolean verification result while still performing semantic evidence review.

## Error consensus

Web status errors, oversized responses, and hash mismatches yield a canonical
`EVIDENCE_UNAVAILABLE` panel whose only verdict is `ABSTAIN`. A validator accepts
that fallback only when its own fetch also fails. Malformed LLM output yields
`MODEL_OUTPUT_INVALID`; it is never eligible for proof-audit approval.

## Precedent comparison

Only resolved cases under the same policy are eligible. Each selected case must
be classified as `APPLY`, `DISTINGUISH`, `CONFLICT`, or `IRRELEVANT`. Omitting or
inventing a precedent makes the panel invalid; an unsupported relation fails
the validator's `PRECEDENT_RELATIONS` obligation.

Precedents are caller-selected rather than discovered by an LLM. This keeps the
bounded consensus input public and prevents nondeterministic search results
from silently changing the decision universe.
