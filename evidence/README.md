# Bounded live-decision evidence

GenLayer web evidence is deliberately bounded to 16,000 bytes per item. The V1
deployed contract source is 26,102 bytes, so this directory preserves the exact
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

## V2 deployment source

The `v2/` directory contains the exact deployed V2 source. It widens only
the validator equivalence rule: once substantive verdict and all precedent
relations match, 3–2 through 5–0 majority strengths are consensus-equivalent.
The original V1 files above remain unchanged.

| Item | Bytes | SHA-256 |
|---|---:|---|
| `v2/precedent_protocol.part-1.py` | 15,000 | `5f9ca6d2759b24fb4f2580c4d643d7ee582c2e35a0434e219413f12fe35f5421` |
| `v2/precedent_protocol.part-2.py` | 11,337 | `71a362ea89f615526afc5961c449eefaad00c1f3b3a722a7e23cc0cecd108c4a` |

Concatenating the V2 parts produces 26,337 bytes and SHA-256
`f0a54d3c751cba7baf949f39afa2c3a5945444677efb774ab659cbfe203e3ff0`.

## V3 deployed source

The `v3/` directory contains the exact V3 source deployed at
[`0x487F08b954b598F47C74524abeE132e27992b268`](https://explorer-studio.genlayer.com/address/0x487F08b954b598F47C74524abeE132e27992b268)
from commit `eb0b23e7ff19216dafe7e29a29b2de12d09e1ca2`. V3 replaces
independent free-form panel regeneration with five bounded semantic proof
obligations over the leader's canonical panel. Validators still fetch and hash
every evidence item independently. Any failed or malformed proof audit rejects
the proposed substantive transition; unavailable evidence is recorded only as
the explicit fail-closed `ABSTAIN` fallback.

| Item | Bytes | SHA-256 |
|---|---:|---|
| `v3/precedent_protocol.part-1.py` | 15,000 | `da783cae7d0d140b1d46f943400222c9773634af3756e49a4732e291b6cc0cb3` |
| `v3/precedent_protocol.part-2.py` | 12,469 | `36631919938dad62faaf33cd80720e41531533f1b8a07a2953d1eb05e1f4d1ce` |

Concatenating the V3 parts produces 27,469 bytes and SHA-256
`fa4f6c3dd434c5043061a7b0c39f58ec18c644c837ad06c3dba8f6d016e04cdb`.
