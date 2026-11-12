"""Verify that bounded evidence parts reconstruct the deployed source."""

from hashlib import sha256
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "contracts" / "precedent_protocol.py"
PARTS = [
    ROOT / "evidence" / "precedent_protocol.part-1.py",
    ROOT / "evidence" / "precedent_protocol.part-2.py",
]
EXPECTED = "cb1fd639af0031cf9deba73e1ffbdb0c57cbf080ef0eb5bc64b6d86497190ef0"


def main() -> None:
    source = SOURCE.read_bytes()
    reconstructed = b"".join(path.read_bytes() for path in PARTS)
    assert reconstructed == source, "evidence parts do not reconstruct source"
    assert sha256(reconstructed).hexdigest() == EXPECTED, "deployed source hash mismatch"
    assert all(path.stat().st_size <= 16_000 for path in PARTS), "evidence part exceeds cap"
    print(f"verified {len(source)} bytes: {EXPECTED}")


if __name__ == "__main__":
    main()
