from pathlib import Path

import chess

from tailorfish.eval import StockfishEvaluator
from tailorfish.analysis import detect_blunders


def test_detects_blunder_from_pgn() -> None:
    pgn_path = Path("tests/fixtures/blunder.pgn")
    with open(pgn_path) as pgn:
        game = chess.pgn.read_game(pgn)

    blunders = detect_blunders(game, StockfishEvaluator, chess.WHITE)

    assert len(blunders) == 1

def test_detects_no_blunder_from_pgn() -> None:
    pgn_path = Path("tests/fixtures/no_blunder.pgn")
    with open(pgn_path) as pgn:
        game = chess.pgn.read_game(pgn)

    blunders = detect_blunders(game, StockfishEvaluator, chess.WHITE)

    assert len(blunders) == 0
