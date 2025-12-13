from pathlib import Path

from tailorfish.analysis import analyze_pgn
from tailorfish.student import MistakeType


def test_detects_blunder_from_pgn() -> None:
    pgn_path = Path("tests/fixture/blunder.pgn")
    profiles = analyze_pgn(pgn_path)
    blunders = [p for p in profiles if p.kind == MistakeType.BLUNDER]

    assert len(blunders) == 1

def test_detects_no_blunder_from_pgn() -> None:
    pgn_path = Path("tests/fixture/no_blunder.pgn")
    profiles = analyze_pgn(pgn_path)
    blunders = [p for p in profiles if p.kind == MistakeType.BLUNDER]

    assert len(blunders) == 0
