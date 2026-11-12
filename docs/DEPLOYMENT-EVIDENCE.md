# Studionet deployment evidence

Status: **deployed and accepted**.

## V3 proof-audited deployment

V3 replaces independent free-form panel regeneration with validator proof
audits over one canonical leader panel. Validators independently re-fetch and
hash-check the evidence, then require all five named audit obligations to pass
before a substantive verdict can be committed.

| Item | Immutable evidence |
|---|---|
| Network | GenLayer Studionet |
| Execution mode | Normal (Full Consensus) |
| Contract | [`0x487F08b954b598F47C74524abeE132e27992b268`](https://explorer-studio.genlayer.com/address/0x487F08b954b598F47C74524abeE132e27992b268) |
| Deployment transaction | [`0x4003195f306b1794c97afdfc1f6cb4b8df339df3f53a67067f8b98d7111a3d53`](https://explorer-studio.genlayer.com/tx/0x4003195f306b1794c97afdfc1f6cb4b8df339df3f53a67067f8b98d7111a3d53) |
| Consensus result | `FINALIZED / ACCEPTED` |
| Deployed source commit | [`eb0b23e7ff19216dafe7e29a29b2de12d09e1ca2`](https://github.com/DTung1291/precedent-protocol/tree/eb0b23e7ff19216dafe7e29a29b2de12d09e1ca2) |
| Contract source | [`contracts/precedent_protocol.py`](https://github.com/DTung1291/precedent-protocol/blob/eb0b23e7ff19216dafe7e29a29b2de12d09e1ca2/contracts/precedent_protocol.py) |
| Source SHA-256 | `fa4f6c3dd434c5043061a7b0c39f58ec18c644c837ad06c3dba8f6d016e04cdb` |

The deployed file is 27,469 bytes. Its two bounded evidence parts reconstruct
that file byte-for-byte and are pinned to the same source commit.

### V3 live proof-audited workflow

Policy 2 states the contract's actual safety boundary precisely: a substantive
`CLAIMANT` or `RESPONDENT` verdict requires independently fetched, hash-bound
evidence and all five audit checks; an explicit `ABSTAIN` round remains an
allowed fail-closed record for unavailable evidence or unusable model output.

| Action | Finalized transaction | Accepted-state result |
|---|---|---|
| Create policy 2 | [`0xbe512e488622969ea45ddcfd026a2487dd5709665e6c5f9d6055dab516109ff1`](https://explorer-studio.genlayer.com/tx/0xbe512e488622969ea45ddcfd026a2487dd5709665e6c5f9d6055dab516109ff1) | Policy count `2` |
| Open case 2 | [`0x88a7c6f1e40646761019da300caa270500afe11965d0fde5ca7455ad4245b94f`](https://explorer-studio.genlayer.com/tx/0x88a7c6f1e40646761019da300caa270500afe11965d0fde5ca7455ad4245b94f) | Commit-pinned V3 evidence accepted |
| Submit respondent response | [`0x7e538f80de347e40ade2c57eeb46ff096db01ca57aedf1e4c86b98a5422102bf`](https://explorer-studio.genlayer.com/tx/0x7e538f80de347e40ade2c57eeb46ff096db01ca57aedf1e4c86b98a5422102bf) | Case became ready |
| Decide case 2 | [`0xa0c1ac70046a0579409407f69cd38b897244ac0bc5caaf1313cdcbbd54dc8ca8`](https://explorer-studio.genlayer.com/tx/0xa0c1ac70046a0579409407f69cd38b897244ac0bc5caaf1313cdcbbd54dc8ca8) | `CLAIMANT`, contestability `0` |

The decision reached consensus in the first leader round. `get_case(2)` returns
`current_round_id=2`, `current_verdict=CLAIMANT`, and
`current_contestability_milli=0`. `get_round(2)` returns `basis_status=OK` and
records that the source directly establishes independent re-fetching, SHA-256
verification, the five proof obligations, deterministic verdict derivation,
and the substantive-write gate.

### Negative-control policy test

Before policy 2, case 1 intentionally tested a stronger claim: that *no* failed
or unavailable audit path may write any state at all. The contract returned
`RESPONDENT` with contestability `0`, because V3 deliberately permits a
normalized `ABSTAIN` record when evidence or model output is unavailable. The
negative result demonstrates that the adjudicator applied the policy instead
of automatically approving its own source.

| Action | Finalized transaction | Result |
|---|---|---|
| Create policy 1 | [`0x353dfc6ec52df753642e2ec70b1be1e6223fb7ddae9273dd1f336bdb9273888e`](https://explorer-studio.genlayer.com/tx/0x353dfc6ec52df753642e2ec70b1be1e6223fb7ddae9273dd1f336bdb9273888e) | `ACCEPTED` |
| Open case 1 | [`0xbbc8bd8c4d686436dec48d2206e3034a7c9c9b2d7be06a5d1a2e35be09600be3`](https://explorer-studio.genlayer.com/tx/0xbbc8bd8c4d686436dec48d2206e3034a7c9c9b2d7be06a5d1a2e35be09600be3) | `ACCEPTED` |
| Submit respondent response | [`0xf789d132e94df915003e622e522114be6a006e3f21435f6a9fc0be17f79469f5`](https://explorer-studio.genlayer.com/tx/0xf789d132e94df915003e622e522114be6a006e3f21435f6a9fc0be17f79469f5) | `ACCEPTED` |
| Decide case 1 | [`0x6bfd9b4bea95987b058032013987d5dfe77b9db4c0112c4ac3f566813e037267`](https://explorer-studio.genlayer.com/tx/0x6bfd9b4bea95987b058032013987d5dfe77b9db4c0112c4ac3f566813e037267) | `RESPONDENT`, contestability `0` |

## V1 deployment

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

## V2 deployment

V2 keeps the fail-closed verdict and precedent-relation checks while treating
all substantive five-lens majority strengths (3–2, 4–1, and 5–0) as one
explicit 0–400 contestability equivalence band. This removes false consensus
failure when validators agree on the outcome and every precedent relation but
differ only in the size of that majority.

| Item | Immutable evidence |
|---|---|
| Network | GenLayer Studionet |
| Execution mode | Normal (Full Consensus) |
| Contract | [`0x2ccDE15D1504F7978fa46C2D82Ed44B603d6C0ec`](https://explorer-studio.genlayer.com/address/0x2ccDE15D1504F7978fa46C2D82Ed44B603d6C0ec) |
| Deployment transaction | [`0x579ca5a0fe5a6cfc318100c027559cd9e30b1c3a6ebf7e631f94bdd174ca1b96`](https://explorer-studio.genlayer.com/tx/0x579ca5a0fe5a6cfc318100c027559cd9e30b1c3a6ebf7e631f94bdd174ca1b96) |
| Consensus result | `ACCEPTED` |
| Deployed source commit | [`767ff13904f20c625845afbf6acb4d9fe409ca47`](https://github.com/DTung1291/precedent-protocol/tree/767ff13904f20c625845afbf6acb4d9fe409ca47) |
| Contract source | [`contracts/precedent_protocol.py`](https://github.com/DTung1291/precedent-protocol/blob/767ff13904f20c625845afbf6acb4d9fe409ca47/contracts/precedent_protocol.py) |
| Source SHA-256 | `f0a54d3c751cba7baf949f39afa2c3a5945444677efb774ab659cbfe203e3ff0` |

The source was transferred to Studio from its exact base64 representation and
verified as 26,337 bytes with the SHA-256 above before deployment. Studio then
reported `ACCEPTED`, `Reached consensus`, and `Contract deployed`.

### V2 live two-party workflow

The deployed V2 contract was exercised through the complete two-party path
with four commit-pinned evidence items. Both party writes finalized, while the
semantic decision exhausted leader rotation without majority agreement:

| Action | Finalized transaction | Result |
|---|---|---|
| Create policy 1 | [`0xd5af680adb3da2e5d293e78b2d11f565d658c7a8f03c8a87003dc35aa6fde938`](https://explorer-studio.genlayer.com/tx/0xd5af680adb3da2e5d293e78b2d11f565d658c7a8f03c8a87003dc35aa6fde938) | `ACCEPTED` |
| Open case 1 | [`0x142d44785277d24574b58cc69a32867398d960025bc65c7a685e493f24a77ce0`](https://explorer-studio.genlayer.com/tx/0x142d44785277d24574b58cc69a32867398d960025bc65c7a685e493f24a77ce0) | `ACCEPTED` |
| Submit respondent response | [`0x220570500ca5f936850e0195903e8d9724cf2c1c1e4022d412a02d0480d2f754`](https://explorer-studio.genlayer.com/tx/0x220570500ca5f936850e0195903e8d9724cf2c1c1e4022d412a02d0480d2f754) | `ACCEPTED` |
| Decide case 1 | [`0xe99ba726ae6737e90f52d5891711d51e0c3dc7cffb24bcf9df26507ca8c375aa`](https://explorer-studio.genlayer.com/tx/0xe99ba726ae6737e90f52d5891711d51e0c3dc7cffb24bcf9df26507ca8c375aa) | `UNDETERMINED` |

The decision rotated the leader after repeated majority disagreement and then
finalized as `UNDETERMINED`. The fail-closed invariant held: immediately after
finalization, accepted-state `get_round_count()` returned `0`, so no verdict,
partial panel, or false approval was appended. This live result is evidence of
safe refusal, not a claim that the V2 scenario reached a substantive verdict.

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

## Bounded evidence and semantic disagreement

Commit
[`0959faa2b8d2082f0b475ba53772c627b015c629`](https://github.com/DTung1291/precedent-protocol/tree/0959faa2b8d2082f0b475ba53772c627b015c629)
adds two evidence parts below the per-item cap. Their byte-for-byte
concatenation reproduces the deployed source and its recorded SHA-256. Case 2
used those parts plus the consensus, state-model, deployment, and threat-model
documents: seven hash-pinned items totaling 35,698 bytes.

| Action | Finalized transaction | Result |
|---|---|---|
| Open case 2 | [`0x2a8c57a7c7d799dc15d583425b325009b8d7468814b214b2c244d6e273854ebe`](https://explorer-studio.genlayer.com/tx/0x2a8c57a7c7d799dc15d583425b325009b8d7468814b214b2c244d6e273854ebe) | `ACCEPTED` |
| Submit response | [`0x7601b89b7cc8cf77cb4f6b5744fc16d0adde2370bbf4c5fc5b96e60e2256eb44`](https://explorer-studio.genlayer.com/tx/0x7601b89b7cc8cf77cb4f6b5744fc16d0adde2370bbf4c5fc5b96e60e2256eb44) | `ACCEPTED` |
| Decide with case 1 as precedent | [`0x960a4e82dbafec18e8d70886214d806771de7e409a1185963d8ea7af426eb326`](https://explorer-studio.genlayer.com/tx/0x960a4e82dbafec18e8d70886214d806771de7e409a1185963d8ea7af426eb326) | `UNDETERMINED` |
| Decide without a precedent | [`0xa111e9c2fa5d3735406155110eb9689329216dc101eed572cca0cccb510f6c67`](https://explorer-studio.genlayer.com/tx/0xa111e9c2fa5d3735406155110eb9689329216dc101eed572cca0cccb510f6c67) | `UNDETERMINED` |

Both decision attempts rotated the leader three times after majority
disagreement, then finalized as `UNDETERMINED`. Removing the precedent did not
remove the disagreement, isolating it to the substantive verdict or derived
contestability rather than precedent classification. The contract correctly
made the non-consensus paths unable to update case state: `get_round_count()`
remained `1`, so case 2 created no false approval or partial decision.

Together the two cases demonstrate both contract-level abstention on invalid
evidence and network-level refusal when independent validator judgments do not
meet the equivalence rule.
