# Precedent Protocol

**Precedent-aware semantic arbitration without pretending uncertainty is certainty.**

Most AI adjudication contracts evaluate one prompt, store one verdict, and
forget how they got there. Precedent Protocol turns prior decisions,
counterarguments, and contestability into reusable on-chain state.

Two named parties submit opposing statements and content-addressed public
evidence. A GenLayer leader evaluates the case through five deliberately
different lenses. Validators independently fetch the same bytes, produce their
own five-lens panel, and accept the proposal only when the substantive verdict,
contestability band, and treatment of every cited precedent agree.

> A decision is more useful when downstream builders can see both what won and
> how difficult the decision was.

This is an agreed arbitration primitive. It is not a legal court and its
application-level review rounds are distinct from GenLayer protocol appeals.

## The primitive

Every decision must include these lenses:

1. `FACTS` — what the bounded evidence actually establishes;
2. `POLICY` — how the immutable standard applies;
3. `ADVERSARIAL` — the strongest case against the apparent result;
4. `PRECEDENT` — whether earlier cases apply or must be distinguished;
5. `REMEDY` — whether the proposed outcome fits the available outcomes.

Contract code derives the verdict from the five opinions. A substantive result
requires at least three matching lenses. A split panel becomes `ABSTAIN`.
`contestability_milli` is derived from the size of the majority, never trusted
from model prose:

| Panel | Verdict | Contestability |
|---|---|---:|
| 5–0 | majority outcome | 0 |
| 4–1 | majority outcome | 200 |
| 3–2 | majority outcome | 400 |
| tie, fragmented, or abstaining majority | `ABSTAIN` | 1000 |

Downstream contracts can require a specific verdict and reject results above
their own contestability threshold.

## Consensus is load-bearing

```text
immutable policy + two parties + hash-bound evidence + selected precedents
                                |
                                v
               leader fetches and verifies exact bytes
                                |
                                v
             five-lens panel + precedent treatments
                                |
                                v
         contract derives verdict and contestability in code
                                |
                                v
           validators independently fetch and deliberate
                                |
                 +--------------+--------------+
                 |                             |
       compatible substance             disagreement
                 |                             |
                 v                             v
       append-only decision round      no state transition
```

Validators do not approve a schema-only response. They independently repeat
the semantic work. A write requires:

- the same derived verdict;
- contestability within the explicit 0–400 substantive-majority band;
- the same `APPLY`, `DISTINGUISH`, `CONFLICT`, or `IRRELEVANT` relation for
  every submitted precedent;
- independently verified evidence bytes matching every submitted SHA-256.

HTTP errors, changed content, oversized evidence, and unavailable sources can
only produce the safe `ABSTAIN` fallback. They cannot produce a favorable
substantive verdict.

## Precedent without ossification

Every resolved case under the same policy may be submitted as precedent. The
panel must address each one explicitly. Precedent is therefore visible and
auditable, but not blindly binding: a materially different case can be
distinguished, and conflicting history must be disclosed.

Up to three rounds may exist for a case. Reviews are append-only and can affirm
or reverse the current verdict. Earlier rounds remain queryable, so a consumer
can distinguish a stable decision from a repeatedly contested one.

## Public API

Writes:

```python
create_policy(name, standard, outcomes_json) -> policy_id
open_case(policy_id, respondent_address, question, claimant_statement,
          evidence_json) -> case_id
submit_response(case_id, respondent_statement, evidence_json)
decide(case_id, review_note, review_evidence_json,
       precedent_ids_json) -> round_id
```

Views:

```python
get_policy_count() -> int
get_case_count() -> int
get_round_count() -> int
get_policy(policy_id) -> dict
get_case(case_id) -> dict
get_round(round_id) -> dict
get_case_rounds(case_id) -> list[int]
```

Evidence is a bounded JSON array. The content hash makes a mutable web URL
fail closed if its bytes change:

```json
[
  {
    "url": "https://example.org/public/delivery-record.txt",
    "sha256": "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef",
    "label": "Signed delivery record"
  }
]
```

## Repository map

```text
contracts/precedent_protocol.py  deployable single-file contract
tests/                           deterministic and consensus-boundary tests
tests_integration/               official gltest network integration checks
gltest.config.yaml               conservative Studionet polling configuration
docs/CONSENSUS.md                leader/validator protocol
docs/STATE-MODEL.md              records, transitions, and invariants
docs/THREAT-MODEL.md             adversaries and residual risk
docs/DEPLOYMENT-EVIDENCE.md      immutable live-run record
DECISIONS.md                     engineering decisions and live findings
```

## Live Studionet deployment

- Contract: [`0x1629868339F7a8305B4E7e5B7d4F70b83e932feD`](https://explorer-studio.genlayer.com/address/0x1629868339F7a8305B4E7e5B7d4F70b83e932feD)
- Deployment transaction: [`0x65cbc74406e66c45bbde611650d2cd7b073e7a5706937ef198c1fc62b24d1582`](https://explorer-studio.genlayer.com/tx/0x65cbc74406e66c45bbde611650d2cd7b073e7a5706937ef198c1fc62b24d1582)
- Deployed source commit: [`4a0d9bef1d618d6d7239b711ee9c269dd5f99f6d`](https://github.com/DTung1291/precedent-protocol/tree/4a0d9bef1d618d6d7239b711ee9c269dd5f99f6d)
- Contract source SHA-256: `cb1fd639af0031cf9deba73e1ffbdb0c57cbf080ef0eb5bc64b6d86497190ef0`

The deployment reached `ACCEPTED` under Studio's Normal (Full Consensus)
execution mode. See [the deployment evidence record](docs/DEPLOYMENT-EVIDENCE.md)
for the exact boundary between completed evidence and planned live scenarios.

## Verify locally

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
./scripts/check.sh
```

The initial suite contains **21 tests** covering party authorization, immutable
policies, evidence hashing, HTTP failure, forced abstention, malformed model
output, validator disagreement, precedent compatibility, append-only review,
reversal, round limits, dedupe, and prompt-injection boundaries.

Official integration checks are separate because they deploy and execute live
validator consensus:

```bash
python3 -m venv .venv-integration
.venv-integration/bin/pip install -r requirements-integration.txt
.venv-integration/bin/gltest --network studionet \
  tests_integration/test_precedent_protocol.py
```

## Hard boundaries

- No funds or automatic legal enforcement.
- No hidden evidence: all submitted material and reasoning are public.
- Content hashing proves which bytes were evaluated, not that a source is
  truthful or independent.
- `contestability_milli` measures dispersion across five required deliberative
  lenses inside each validator execution; it is not a count of protocol votes.
- A result applies only to the registered policy, parties, question, evidence,
  and selected precedents.
- Protocol-level appeals can still challenge the transaction before finality.

## License

MIT
