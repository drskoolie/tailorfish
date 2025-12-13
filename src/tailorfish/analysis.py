from pathlib import Path

import chess.pgn

from tailorfish.eval import StockfishEvaluator
from tailorfish.student import MistakeProfile, MistakeType

pgn_path = Path("tests/fixtures/blunder.pgn")
engine_path = Path("/usr/games/stockfish")

with open(pgn_path) as pgn:
    game = chess.pgn.read_game(pgn)

board = game.board()
with StockfishEvaluator(engine_path=engine_path, depth=10) as ev:
    cp = ev.eval_cp(board)
    print(cp)
    print(board)

def analyze_pgn(path: Path) -> list[MistakeProfile]:
    return [
            MistakeProfile(
                kind=MistakeType.BLUNDER,
                frequency=1,
                avg_centipawn_loss=300.0,
                typical_move_number = 3,
                )
            ]
