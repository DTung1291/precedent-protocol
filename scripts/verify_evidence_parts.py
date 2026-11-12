"""Verify bounded deployed sources and the current V3 source evidence."""

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
V3_PARTS = [
    ROOT / "evidence" / "v3" / "precedent_protocol.part-1.py",
    ROOT / "evidence" / "v3" / "precedent_protocol.part-2.py",
]
V1_EXPECTED = "cb1fd639af0031cf9deba73e1ffbdb0c57cbf080ef0eb5bc64b6d86497190ef0"
V2_EXPECTED = "f0a54d3c751cba7baf949f39afa2c3a5945444677efb774ab659cbfe203e3ff0"
V3_EXPECTED = "fa4f6c3dd434c5043061a7b0c39f58ec18c644c837ad06c3dba8f6d016e04cdb"


def main() -> None:
    v1_source = b"".join(path.read_bytes() for path in V1_PARTS)
    v2_source = b"".join(path.read_bytes() for path in V2_PARTS)
    v3_source = b"".join(path.read_bytes() for path in V3_PARTS)
    assert sha256(v1_source).hexdigest() == V1_EXPECTED, "V1 deployed source hash mismatch"
    assert sha256(v2_source).hexdigest() == V2_EXPECTED, "V2 source hash mismatch"
    assert v3_source == CURRENT_SOURCE.read_bytes(), "V3 parts do not reconstruct current source"
    assert sha256(v3_source).hexdigest() == V3_EXPECTED, "V3 source hash mismatch"
    assert all(
        path.stat().st_size <= 16_000 for path in V1_PARTS + V2_PARTS + V3_PARTS
    ), "evidence part exceeds cap"
    print(f"verified V1 {len(v1_source)} bytes: {V1_EXPECTED}")
    print(f"verified V2 {len(v2_source)} bytes: {V2_EXPECTED}")
    print(f"verified V3 {len(v3_source)} bytes: {V3_EXPECTED}")


if __name__ == "__main__":
    main()
