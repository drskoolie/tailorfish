from pathlib import Path

import chess.pgn

from tailorfish.eval import StockfishEvaluator

pgn_path = Path("tests/fixtures/blunder.pgn")
engine_path = Path("/usr/games/stockfish")

with open(pgn_path) as pgn:
    game = chess.pgn.read_game(pgn)

def detect_blunders(
        game: chess.pgn.Game,
        eval: StockfishEvaluator,
        target: chess.Color,
        blunder_cp: int = 200,
        ) -> list:
    board = game.board()

    blunders: list[int, int, int] = [] # [move_number, ply, harm]

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
                blunders.append([int(board.fullmove_number), int(board.ply()), int(harm)])

    return blunders

detect_blunders(game=game, eval= StockfishEvaluator, target=chess.WHITE)
