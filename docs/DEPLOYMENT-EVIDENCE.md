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

## Live fail-closed scenario

The first full two-party workflow is finalized on Studionet:

| Action | Finalized transaction |
|---|---|
| Create policy | [`0x86fe014b6a71f80c8d9ce1e89377e6634b16db6a2ad8afde14fe2b848d6126e0`](https://explorer-studio.genlayer.com/tx/0x86fe014b6a71f80c8d9ce1e89377e6634b16db6a2ad8afde14fe2b848d6126e0) |
| Open case 1 | [`0x9430300da998df0e1cb0851f7b3cfc7fe1d48062112f7e2ce6825f0bccc7f011`](https://explorer-studio.genlayer.com/tx/0x9430300da998df0e1cb0851f7b3cfc7fe1d48062112f7e2ce6825f0bccc7f011) |
| Submit response | [`0x4166b5b68cf2330bab9c6f9ef63886a32ced30c6faa4eb684034b2db26ba4700`](https://explorer-studio.genlayer.com/tx/0x4166b5b68cf2330bab9c6f9ef63886a32ced30c6faa4eb684034b2db26ba4700) |
| Decide round 1 | [`0x24c26fc561f3983a494d98a000338bd0eac9d96bec11f0225b4ae9b0a19dc491`](https://explorer-studio.genlayer.com/tx/0x24c26fc561f3983a494d98a000338bd0eac9d96bec11f0225b4ae9b0a19dc491) |

Case 1 intentionally exposed the runtime boundary: the 26,102-byte source file
exceeded the 16,000-byte per-item cap. `get_round(1)` therefore returns
`basis_status=EVIDENCE_UNAVAILABLE`, `verdict=ABSTAIN`,
`contestability_milli=1000`, five `ABSTAIN` opinions, and the reason
`ValueError: evidence exceeds per-item byte limit`. This demonstrates that an
oversized or unavailable source cannot produce a substantive approval.

The repository now includes bounded source parts and a reconstruction check for
a second substantive live case. Additional transactions are recorded only once
they finalize.
