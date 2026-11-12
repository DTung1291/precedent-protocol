# Bounded live-decision evidence

GenLayer web evidence is deliberately bounded to 16,000 bytes per item. The
deployed contract source is 26,102 bytes, so this directory exposes the exact
source as two immutable, independently hashable items for live adjudication.

| Item | Lines | Bytes | SHA-256 |
|---|---:|---:|---|
| `precedent_protocol.part-1.py` | 1-294 | 11,601 | `56f51ff2e6de109f088fbf36cbaf58c6e965394649b3f90add8ad6d72eac79bf` |
| `precedent_protocol.part-2.py` | 295-588 | 14,501 | `e9f127cb109299944f194ec1e599d83189795d673adf2bd47263c511df7bec21` |

Concatenating part 1 and part 2 without modification produces 26,102 bytes and
SHA-256 `cb1fd639af0031cf9deba73e1ffbdb0c57cbf080ef0eb5bc64b6d86497190ef0`.
That is the hash recorded for the source deployed at
`0x1629868339F7a8305B4E7e5B7d4F70b83e932feD`.

Reproduce the check from the repository root:

```sh
python3 scripts/verify_evidence_parts.py
```

The split is only a transport representation for the contract's bounded web
reader. The deployable source of record remains
`contracts/precedent_protocol.py`.
