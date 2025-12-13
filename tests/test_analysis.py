from pathlib import Path

import chess

from tailorfish.analysis import detect_blunders, detect_missed_moves
from tailorfish.eval import StockfishEvaluator


def test_detect_blunder_true() -> None:
    pgn_path = Path("tests/fixtures/blunder.pgn")
    with open(pgn_path) as pgn:
        game = chess.pgn.read_game(pgn)

    blunders = detect_blunders(game, StockfishEvaluator, chess.WHITE)

    assert len(blunders) == 1

def test_detect_blunder_false() -> None:
    pgn_path = Path("tests/fixtures/no_blunder.pgn")
    with open(pgn_path) as pgn:
        game = chess.pgn.read_game(pgn)

    blunders = detect_blunders(game, StockfishEvaluator, chess.WHITE)

    assert len(blunders) == 0

def test_detect_missed_move_true() -> None:
    pgn_path = Path("tests/fixtures/missed_move.pgn")
    with open(pgn_path) as pgn:
        game = chess.pgn.read_game(pgn)

    missed_moves = detect_missed_moves(game, StockfishEvaluator, chess.WHITE)

    assert len(missed_moves) == 1


def test_detect_missed_move_false() -> None:
    pgn_path = Path("tests/fixtures/no_blunder.pgn")
    with open(pgn_path) as pgn:
        game = chess.pgn.read_game(pgn)

    missed_moves = detect_missed_moves(game, StockfishEvaluator, chess.WHITE)

    assert len(missed_moves) == 0
