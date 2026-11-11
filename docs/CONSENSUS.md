# Consensus protocol

## Decision-bearing fields

The leader may use natural-language reasoning, but contract code recognizes
only bounded fields: five lens verdicts, explicit precedent relations, and
short explanations. The final verdict and contestability are derived in code.

Validators independently fetch every evidence URL and verify its SHA-256. They
then run the same five-lens task without being instructed to defer to the
leader. Consensus accepts only when:

1. both panels normalize safely;
2. both panels derive the same verdict;
3. contestability differs by at most 250 milli-points; and
4. every precedent receives the same semantic relation.

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

## Error consensus

Web status errors, oversized responses, and hash mismatches yield a canonical
`EVIDENCE_UNAVAILABLE` panel whose only verdict is `ABSTAIN`. A validator accepts
that fallback only when its own fetch also fails. Malformed LLM output yields
`MODEL_OUTPUT_INVALID`; it is never accepted against a valid independent
panel.

## Precedent comparison

Only resolved cases under the same policy are eligible. Each selected case must
be classified as `APPLY`, `DISTINGUISH`, `CONFLICT`, or `IRRELEVANT`. Omitting a
precedent, inventing one, or disagreeing on its relation prevents the write.

Precedents are caller-selected rather than discovered by an LLM. This keeps the
bounded consensus input public and prevents nondeterministic search results
from silently changing the decision universe.
