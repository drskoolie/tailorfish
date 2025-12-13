import math
from dataclasses import dataclass
from pathlib import Path

import chess.pgn

from tailorfish.eval import StockfishEvaluator


@dataclass
class GameEvaluator:
    engine_path: Path = Path("/usr/games/stockfish")
    evaluator: type[StockfishEvaluator] = StockfishEvaluator

    def __init__(self) -> None:
        self.depth = 10
        self.blunders_threshold_cp = 200
        self.missed_moves_threshold_cp = 200
    
    def set_game(self, pgn_path: Path, target: chess.Color) -> None:
        with open(pgn_path) as pgn:
            self.game = chess.pgn.read_game(pgn)
        self.target = target

    def move_analyzer(self):
        if self.game is None:
            raise ValueError("Input game is not set")

        board = self.game.board()

        data: list[dict[str, object]] = []

        with self.evaluator(engine_path=self.engine_path, depth=self.depth) as ev:
            for move in self.game.mainline_moves():
                mover = board.turn

                san = board.san(move)
                if mover == self.target:
                    best_move = ev.get_best_move(board)
                    best_move_uci = best_move.uci()
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
                    delta_player = math.nan
                    delta_best_move = math.nan
                    board.push(move)

                data.append(
                        {
                            "ply": board.ply(),
                            "fullmove": board.fullmove_number,
                            "mover": "W" if mover == chess.WHITE else "B",
                            "uci": move.uci(),
                            "san": san,
                            "cp_before": int(cp_before),
                            "cp_after": int(cp_after),
                            "delta_player": delta_player,
                            "best_move_uci": best_move_uci,
                            "cp_best_move": cp_best_move,
                            "delta_best_move": delta_best_move,
                        }
                    )
        return data


if __name__ == "__main__":
    pgn_path_blunder = Path("tests/fixtures/blunder.pgn")
    pgn_path_missed = Path("tests/fixtures/missed_move.pgn")

    ge = GameEvaluator()
    ge.set_game(pgn_path_blunder, chess.WHITE)
    ge.move_analyzer()
    ge.set_game(pgn_path_missed, chess.WHITE)
    ge.move_analyzer()
