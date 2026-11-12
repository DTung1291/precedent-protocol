"""Verify bounded V1 deployment evidence and the current V2 source evidence."""

from hashlib import sha256
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CURRENT_SOURCE = ROOT / "contracts" / "precedent_protocol.py"
V1_PARTS = [
    ROOT / "evidence" / "precedent_protocol.part-1.py",
    ROOT / "evidence" / "precedent_protocol.part-2.py",
]
V2_PARTS = [
    ROOT / "evidence" / "v2" / "precedent_protocol.part-1.py",
    ROOT / "evidence" / "v2" / "precedent_protocol.part-2.py",
]
V1_EXPECTED = "cb1fd639af0031cf9deba73e1ffbdb0c57cbf080ef0eb5bc64b6d86497190ef0"
V2_EXPECTED = "f0a54d3c751cba7baf949f39afa2c3a5945444677efb774ab659cbfe203e3ff0"


def main() -> None:
    v1_source = b"".join(path.read_bytes() for path in V1_PARTS)
    v2_source = b"".join(path.read_bytes() for path in V2_PARTS)
    assert sha256(v1_source).hexdigest() == V1_EXPECTED, "V1 deployed source hash mismatch"
    assert v2_source == CURRENT_SOURCE.read_bytes(), "V2 parts do not reconstruct current source"
    assert sha256(v2_source).hexdigest() == V2_EXPECTED, "V2 source hash mismatch"
    assert all(
        path.stat().st_size <= 16_000 for path in V1_PARTS + V2_PARTS
    ), "evidence part exceeds cap"
    print(f"verified V1 {len(v1_source)} bytes: {V1_EXPECTED}")
    print(f"verified V2 {len(v2_source)} bytes: {V2_EXPECTED}")


if __name__ == "__main__":
    main()
