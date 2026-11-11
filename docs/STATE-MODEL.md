# State model

## Policy

Policies are immutable and content-addressed. A policy defines a natural-
language standard plus two to four outcome labels. `ABSTAIN` is reserved by the
protocol and cannot be registered as a substantive outcome.

## Case

```text
AWAITING_RESPONSE --submit_response--> READY --decide--> RESOLVED
                                                   |
                                                   +-- review --> RESOLVED
```

A case names one claimant and one respondent. The respondent address is fixed
when the case opens, preventing an unrelated address from supplying the
counterargument. The question, statements, and initial evidence are never
edited after submission.

The case stores only a pointer to its current round plus a derived current
verdict and contestability. Historical rounds remain in separate append-only
records.

## Decision round

Each round binds:

- case ID and prior round ID;
- requester address;
- optional review challenge and new hash-bound evidence;
- explicit precedent case IDs;
- the consensus-agreed panel;
- derived verdict and contestability inside that panel;
- timestamp and request hash.

At most three rounds may be written. A review can reverse the current result,
but never mutates an earlier round.

## Invariants

1. Only the named respondent can move a case to `READY`.
2. Only a named party can request a decision or review.
3. No substantive verdict is stored after evidence fetch/hash failure.
4. Every substantive verdict has exactly five distinct required lenses.
5. Verdict and contestability are deterministic functions of lens votes.
6. Every cited precedent is resolved under the same immutable policy.
7. Every precedent is treated exactly once.
8. Decision history is append-only and bounded to three rounds.
9. Validator disagreement produces no state change.
