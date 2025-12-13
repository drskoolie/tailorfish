from pathlib import Path

import chess.engine
import chess.pgn

from tailorfish.student import MistakeProfile, MistakeType

path = Path("tests/fixtures/blunder.pgn")
with open(path) as pgn:
    game = chess.pgn.read_game(pgn)

board = game.board()

engine = chess.engine.SimpleEngine.popen_uci("/usr/games/stockfish")

info = engine.analyse(board, chess.engine.Limit(depth=10))

score = info["score"].pov(board.turn)
cp = score.score(mate_score=10000)


def analyze_pgn(path: Path) -> list[MistakeProfile]:
    return [
            MistakeProfile(
                kind=MistakeType.BLUNDER,
                frequency=1,
                avg_centipawn_loss=300.0,
                typical_move_number = 3,
                )
            ]
