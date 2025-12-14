from pathlib import Path

import chess
import polars as pl

from tailorfish.analysis import GameEvaluator


def test_detect_blunder_true() -> None:
    pgn_path = Path("tests/fixtures/blunder.pgn")

    ge = GameEvaluator()
    ge.load_game_from_path(pgn_path, chess.WHITE)

    df = ge.move_analyzer()

    assert df["delta_player"][4] <= -500

def test_detect_blunder_false() -> None:
    pgn_path = Path("tests/fixtures/no_blunder.pgn")

    ge = GameEvaluator()
    ge.load_game_from_path(pgn_path, chess.WHITE)

    df = ge.move_analyzer()

    assert (
            df
            .filter(pl.col("delta_player").is_not_null())
            .select(pl.col("delta_player").min())
            .item()
            >= -500
            )


def test_detect_missed_move_true() -> None:
    pgn_path = Path("tests/fixtures/missed_move.pgn")

    ge = GameEvaluator()
    ge.load_game_from_path(pgn_path, chess.WHITE)

    df = ge.move_analyzer()

    assert df["delta_best_move"][6] >= 10000


def test_detect_missed_move_false() -> None:
    pgn_path = Path("tests/fixtures/no_blunder.pgn")

    ge = GameEvaluator()
    ge.load_game_from_path(pgn_path, chess.WHITE)

    df = ge.move_analyzer()

    assert (
            df
            .filter(pl.col("delta_best_move").is_not_null())
            .select(pl.col("delta_best_move").min())
            .item()
            <= 500
            )
