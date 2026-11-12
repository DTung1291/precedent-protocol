# Engineering decisions

## D-001 — One flagship primitive

Precedent Protocol is one deep contract rather than a catalog of loosely
related examples. Policy, adversarial participation, evidence binding,
deliberative dispersion, precedent, and review form one coherent state machine.

## D-002 — Arbitration, not legal authority

The contract is framed as an agreed arbitration primitive. It does not call
itself a legal court, determine jurisdiction, or claim that an on-chain result
is legally binding.

## D-003 — Contestability is derived

Models return five bounded opinions. Contract code derives both the majority
verdict and `contestability_milli`. The score therefore cannot contradict the
panel stored beside it.

## D-004 — Precedent is explicit input

Parties select a bounded list of prior same-policy cases. The leader must state
whether each applies, conflicts, is distinguishable, or is irrelevant, and
validators must affirm that each stated relation is supported. The contract
does not perform nondeterministic precedent search.

## D-005 — Reviews append, never overwrite

Application-level review rounds may change the current verdict but always point
back to the earlier round. This preserves the evolution of a contested result.

## D-006 — Content hashes bind general web evidence

The protocol supports public HTTPS sources beyond GitHub while refusing to
trust mutable URLs. Validators fetch the URL and require the exact submitted
SHA-256. Changed or unavailable bytes produce only `ABSTAIN`.

## D-007 — Use the validated runner, not the advertised newest runner

The linter advertised runner
`1zr6nqk597d97kg0dyxg0shhrykx5v02zjgnyrajapy4wlqvfvwh`, but
`genvm-linter 0.11.0` could not load it (`No module named genlayer.py`). The
contract therefore pins the runner already validated by Studio and the local
toolchain. A runner upgrade will be a separately tested change, never a
metadata-only edit.

## D-008 — Verify a proof-carrying panel instead of regenerating it

V2 asked every validator to generate a complete independent five-lens panel.
The live run safely refused to finalize, but free-form panel regeneration made
liveness depend on multiple models choosing the same outcome labels. V3 keeps
the leader's canonical, deterministically scored panel and makes validators
audit five bounded proof obligations against independently fetched evidence.
Any unsupported or malformed audit still rejects the write; validators cannot
repair the proposal or substitute their own verdict.
