# Threat model

| Threat | Mitigation |
|---|---|
| One-sided case framing | Named respondent must submit a separate statement |
| Evidence changes after submission | Every URL is bound to an expected SHA-256 |
| HTTP failure becomes approval | Fetch failure can only produce `ABSTAIN` |
| Prompt injection in evidence | Prompts label all case/evidence text as untrusted data |
| Leader invents a result | Validators independently fetch and deliberate |
| Schema-only validator | Validator compares verdict, contestability, and precedent relations |
| Model supplies confidence directly | Contract derives contestability from five lens votes |
| Precedent laundering | Only resolved same-policy cases are accepted |
| Hidden precedent omission | Caller submits a bounded explicit precedent set visible on-chain |
| History rewrite | Every decision and review is append-only |
| Review spam | Only parties may review; maximum three rounds; request hashes dedupe |
| Oversized evidence | Per-item, total-byte, item-count, and prose limits |

## Residual risks

- Five model-generated lenses are not five human experts or five validator
  votes. They are a structured deliberation technique.
- SHA-256 binds bytes but cannot prove that a source is honest, complete, or
  independent.
- Parties may omit relevant evidence or precedents. Consumers should treat the
  stored bounded record as the complete decision universe, not a universal
  truth claim.
- Semantically close cases can still be distinguished differently by models.
  Exact relation agreement reduces inconsistency but may reduce liveness.
- Public evidence can disappear. Safe abstention preserves correctness but not
  availability.
- The primitive does not create legal rights, jurisdiction, or enforceability.
