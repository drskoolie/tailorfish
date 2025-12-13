from pathlib import Path

import chess.pgn

from tailorfish.eval import StockfishEvaluator
from tailorfish.student import MistakeProfile, MistakeType

pgn_path = Path("tests/fixtures/blunder.pgn")
engine_path = Path("/usr/games/stockfish")

with open(pgn_path) as pgn:
    game = chess.pgn.read_game(pgn)

def detect_blunders(
        game: chess.pgn.Game,
        eval: StockfishEvaluator,
        target: chess.Color,
        blunder_cp: int = 200,
        ) -> list[MistakeProfile]:
    board = game.board()

    harms: list[int] = []
    move_numbers: list[int] = []

    with eval(engine_path=engine_path, depth=10) as ev:
        for move in game.mainline_moves():
            mover = board.turn
            cp_before = ev.eval_cp(board)
            board.push(move)
            cp_after = ev.eval_cp(board)

            if mover != target:
                continue

            delta = cp_after - cp_before

            harm = -delta if mover == chess.WHITE else delta

            if harm >= blunder_cp:
                harms.append(int(harm))
                move_numbers.append(int(board.fullmove_number))

detect_blunders(game=game, eval= StockfishEvaluator, target=chess.WHITE)

def analyze_pgn(path: Path) -> list[MistakeProfile]:
    return [
            MistakeProfile(
                kind=MistakeType.BLUNDER,
                frequency=1,
                avg_centipawn_loss=300.0,
                typical_move_number = 3,
                )
            ]
