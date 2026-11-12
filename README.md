# Precedent Protocol

**Precedent-aware semantic arbitration without pretending uncertainty is certainty.**

Most AI adjudication contracts evaluate one prompt, store one verdict, and
forget how they got there. Precedent Protocol turns prior decisions,
counterarguments, and contestability into reusable on-chain state.

Two named parties submit opposing statements and content-addressed public
evidence. A GenLayer leader evaluates the case through five deliberately
different lenses. Validators independently fetch the same bytes and audit the
proposal against five explicit proof obligations. A substantive report is
stored only when every validator audit supports its evidence, policy
application, counterargument, precedent treatment, and deterministically
derived verdict. Evidence or model failures may persist only as an explicitly
labelled `ABSTAIN` record, never as substantive approval.

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
          validators independently fetch and proof-audit
                                |
                 +--------------+--------------+
                 |                             |
       all checks supported          any failed check
                 |                             |
                 v                             v
     substantive decision round        transaction rejected

       fetch/model unavailable -> explicit ABSTAIN round
```

Validators do not approve a schema-only response and do not generate a second,
potentially unrelated verdict. They independently audit the proposed reasoning.
A substantive write requires all five proof obligations to pass:

- every material claim is supported by independently verified evidence bytes;
- the immutable policy standard is applied;
- the strongest material counterargument is fairly addressed;
- every `APPLY`, `DISTINGUISH`, `CONFLICT`, or `IRRELEVANT` relation is supported;
- lens votes support the verdict and contestability derived by contract code.

HTTP errors, changed content, oversized evidence, and unavailable sources can
only produce the safe, non-substantive `ABSTAIN` fallback. A malformed or
unsupported audit cannot approve a leader proposal. Neither path can produce a
favorable substantive verdict.

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

- V3 contract: [`0x487F08b954b598F47C74524abeE132e27992b268`](https://explorer-studio.genlayer.com/address/0x487F08b954b598F47C74524abeE132e27992b268)
- Deployment transaction: [`0x4003195f306b1794c97afdfc1f6cb4b8df339df3f53a67067f8b98d7111a3d53`](https://explorer-studio.genlayer.com/tx/0x4003195f306b1794c97afdfc1f6cb4b8df339df3f53a67067f8b98d7111a3d53)
- Deployed source commit: [`eb0b23e7ff19216dafe7e29a29b2de12d09e1ca2`](https://github.com/DTung1291/precedent-protocol/tree/eb0b23e7ff19216dafe7e29a29b2de12d09e1ca2)
- Contract source SHA-256: `fa4f6c3dd434c5043061a7b0c39f58ec18c644c837ad06c3dba8f6d016e04cdb`
- Proof-audited decision: [`0xa0c1ac70046a0579409407f69cd38b897244ac0bc5caaf1313cdcbbd54dc8ca8`](https://explorer-studio.genlayer.com/tx/0xa0c1ac70046a0579409407f69cd38b897244ac0bc5caaf1313cdcbbd54dc8ca8) — `CLAIMANT`, contestability `0`

The deployment reached `ACCEPTED` under Studio's Normal (Full Consensus)
execution mode. A complete V3 two-party workflow then finalized a five-lens,
proof-audited decision in its first leader round. Accepted-state reads return
`basis_status=OK`, `current_verdict=CLAIMANT`, and
`current_contestability_milli=0`. See
[the deployment evidence record](docs/DEPLOYMENT-EVIDENCE.md) for every
transaction and the deliberately over-strict policy test that the same
contract rejected. V1 and V2 remain documented there for reproducibility.

## Verify locally

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
./scripts/check.sh
```

The suite contains **22 tests** covering party authorization, immutable
policies, evidence hashing, HTTP failure, forced abstention, malformed model
output, failed or malformed proof audits, precedent compatibility, append-only review,
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
