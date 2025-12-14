from dataclasses import dataclass
from io import StringIO
from pathlib import Path
from typing import TypedDict

import chess.pgn
import polars as pl

from tailorfish.eval import StockfishEvaluator


class GameRecord(TypedDict):
    game: chess.pgn.Game
    target: chess.Color

def load_games_into_ram(pgn_path: Path) -> list[GameRecord]:
    text = pgn_path.read_text(encoding="utf-8")

    games: list[GameRecord] = []
    buf = StringIO(text)

    while (game := chess.pgn.read_game(buf)) is not None:
        target = chess.WHITE if game.headers["White"] == "drskoolie" else chess.BLACK
        games.append({"game": game, "target": target})

    return games

@dataclass
class GameEvaluator:
    engine_path: Path = Path("/usr/games/stockfish")
    evaluator: type[StockfishEvaluator] = StockfishEvaluator

    def __init__(self) -> None:
        self.depth = 10
        self.blunders_threshold_cp = 200
        self.missed_moves_threshold_cp = 200
    

    def load_game_from_path(self, pgn_path: Path, target: chess.Color) -> None:
        with open(pgn_path) as pgn:
            self.game = chess.pgn.read_game(pgn)
        self.target = target

    def load_game_directly(self, game: chess.pgn.Game, target: chess.Color) -> None:
        self.game = game
        self.target = target

    def move_analyzer(self) -> pl.DataFrame:
        if self.game is None:
            raise ValueError("Input game is not set")

        board = self.game.board()

        rows: list[dict[str, object]] = []

        with self.evaluator(engine_path=self.engine_path, depth=self.depth) as ev:
            for move in self.game.mainline_moves():
                mover = board.turn

                san = board.san(move)
                if mover == self.target:
                    best_move = ev.get_best_move(board)
                    best_move_uci = best_move.uci()
                    best_move_san = board.san(best_move)
                    board.push(best_move)
                    cp_best_move = ev.eval_cp(board)
                    board.pop()

                    cp_before = ev.eval_cp(board)
                    board.push(move)
                    cp_after = ev.eval_cp(board)
                    delta_player = cp_after - cp_before
                    delta_best_move = cp_best_move - cp_after

                    if mover == chess.BLACK:
                        delta_player = -delta_player
                        delta_best_move = -delta_best_move
                else:
                    delta_player = None
                    delta_best_move = None
                    best_move = None
                    best_move_uci = None
                    best_move_san = None
                    cp_best_move = None
                    cp_before = None
                    cp_after = None
                    board.push(move)

                rows.append(
                        {
                            "ply": board.ply(),
                            "fullmove": board.fullmove_number,
                            "mover": "W" if mover == chess.WHITE else "B",
                            "uci": move.uci(),
                            "san": san,
                            "cp_before": cp_before,
                            "cp_after": cp_after,
                            "delta_player": delta_player,
                            "best_move_uci": best_move_uci,
                            "best_move_san": best_move_san,
                            "cp_best_move": cp_best_move,
                            "delta_best_move": delta_best_move,
                        }
                    )
        return pl.DataFrame(rows)


if __name__ == "__main__":
    pgn_path_drskoolie = Path("data/raw/lichess_drskoolie_2025-12-14.pgn")
    games = load_games_into_ram(pgn_path_drskoolie)

    ge = GameEvaluator()
    ge.load_game_directly(games[0]["game"], games[0]["target"])
    df = ge.move_analyzer()
