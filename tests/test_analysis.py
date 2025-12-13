from pathlib import Path

import chess

from tailorfish.analysis import GameEvaluator


def test_detect_blunder_true() -> None:
    pgn_path = Path("tests/fixtures/blunder.pgn")

    ge = GameEvaluator()
    ge.set_game(pgn_path, chess.WHITE)

    blunders = ge.detect_blunders()

    assert len(blunders) == 1

def test_detect_blunder_false() -> None:
    pgn_path = Path("tests/fixtures/no_blunder.pgn")

    ge = GameEvaluator()
    ge.set_game(pgn_path, chess.WHITE)

    blunders = ge.detect_blunders()

    assert len(blunders) == 0

def test_detect_missed_move_true() -> None:
    pgn_path = Path("tests/fixtures/missed_move.pgn")

    ge = GameEvaluator()
    ge.set_game(pgn_path, chess.WHITE)

    missed_moves = ge.detect_missed_moves()

    assert len(missed_moves) == 1


def test_detect_missed_move_false() -> None:
    pgn_path = Path("tests/fixtures/no_blunder.pgn")

    ge = GameEvaluator()
    ge.set_game(pgn_path, chess.WHITE)

    missed_moves = ge.detect_missed_moves()

    assert len(missed_moves) == 0
