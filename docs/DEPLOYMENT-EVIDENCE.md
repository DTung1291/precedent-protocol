# Studionet deployment evidence

Status: **deployed and accepted**.

## Deployment

| Item | Immutable evidence |
|---|---|
| Network | GenLayer Studionet |
| Execution mode | Normal (Full Consensus) |
| Contract | [`0x1629868339F7a8305B4E7e5B7d4F70b83e932feD`](https://explorer-studio.genlayer.com/address/0x1629868339F7a8305B4E7e5B7d4F70b83e932feD) |
| Deployment transaction | [`0x65cbc74406e66c45bbde611650d2cd7b073e7a5706937ef198c1fc62b24d1582`](https://explorer-studio.genlayer.com/tx/0x65cbc74406e66c45bbde611650d2cd7b073e7a5706937ef198c1fc62b24d1582) |
| Consensus result | `ACCEPTED` |
| Deployed source commit | [`4a0d9bef1d618d6d7239b711ee9c269dd5f99f6d`](https://github.com/DTung1291/precedent-protocol/tree/4a0d9bef1d618d6d7239b711ee9c269dd5f99f6d) |
| Contract source | [`contracts/precedent_protocol.py`](https://github.com/DTung1291/precedent-protocol/blob/4a0d9bef1d618d6d7239b711ee9c269dd5f99f6d/contracts/precedent_protocol.py) |
| Source SHA-256 | `cb1fd639af0031cf9deba73e1ffbdb0c57cbf080ef0eb5bc64b6d86497190ef0` |

Studio exposed all seven read methods and all four write methods after the
deployment reached consensus. The source was hash-checked before it was loaded
into Studio; the hash above is the exact deployed single-file contract.

## Live scenario evidence still to record

Deployment is complete. The following application transactions are deliberately
not claimed yet and will be added only after their live runs finalize:

- a policy, two-party case, response, and first decision;
- a related case that explicitly treats the first case as precedent;
- an append-only review round that affirms or reverses a result;
- exact public evidence URLs and content hashes for those cases;
- `get_case`, `get_round`, and `get_case_rounds` outputs;
- notable leader rotation, abstention, or validator disagreement findings.
