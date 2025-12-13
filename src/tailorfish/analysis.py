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

    def detect_blunders(self) -> list[tuple[int, int, int]]:
        if self.game is None:
            raise ValueError("Input game is not set")

        board = self.game.board()

        blunders: list[tuple[int, int, int]] = [] # [move_number, ply, harm]

        with self.evaluator(engine_path=self.engine_path, depth=self.depth) as ev:
            for move in self.game.mainline_moves():
                mover = board.turn
                cp_before = ev.eval_cp(board)
                board.push(move)
                cp_after = ev.eval_cp(board)

                if mover != self.target:
                    continue

                delta = cp_after - cp_before

                harm = -delta if mover == chess.WHITE else delta

                if harm >= self.blunders_threshold_cp:
                    blunders.append((int(board.fullmove_number), int(board.ply()), int(harm)))

        return blunders

    def detect_missed_moves(self) -> list[tuple[int, int, int]]:
        if self.game is None:
            raise ValueError("Input game is not correct")

        board = self.game.board()

        missed_moves: list[tuple[int, int, int]] = [] # [move_number, ply, harm]

        with self.evaluator(engine_path=self.engine_path, depth=self.depth) as ev:
            for move in self.game.mainline_moves():
                mover = board.turn
                if mover == self.target:
                    best_move = ev.get_best_move(board)
                    board.push(best_move)
                    cp_best_move = ev.eval_cp(board)

                    board.pop()
                    board.push(move)
                    cp_chosen_move = ev.eval_cp(board)

                    delta = cp_best_move - cp_chosen_move
                    missed_move = delta if mover == chess.WHITE else -delta

                    if missed_move >= self.missed_moves_threshold_cp:
                        missed_moves.append((int(board.fullmove_number), int(board.ply()), int(missed_move)))

                else:
                    board.push(move)

        return missed_moves



if __name__ == "__main__":
    pgn_path_blunder = Path("tests/fixtures/blunder.pgn")
    pgn_path_missed = Path("tests/fixtures/missed_move.pgn")

    ge = GameEvaluator()
    ge.set_game(pgn_path_blunder, chess.WHITE)
    ge.detect_blunders()
    ge.set_game(pgn_path_missed, chess.WHITE)
    ge.detect_missed_moves()
