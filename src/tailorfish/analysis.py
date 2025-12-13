from pathlib import Path

import chess.pgn

from tailorfish.eval import StockfishEvaluator

engine_path = Path("/usr/games/stockfish")

def detect_blunders(
        game: chess.pgn.Game | None,
        eval: type[StockfishEvaluator],
        target: chess.Color,
        loss_threshold_cp: int = 200,
        ) -> list[tuple[int, int, int]]:

    if game is None:
        raise ValueError("Input game is not correct")

    board = game.board()

    blunders: list[tuple[int, int, int]] = [] # [move_number, ply, harm]

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

            if harm >= loss_threshold_cp:
                blunders.append((int(board.fullmove_number), int(board.ply()), int(harm)))

    return blunders

def detect_missed_moves(
        game: chess.pgn.Game | None,
        eval: type[StockfishEvaluator],
        target: chess.Color,
        loss_threshold_cp: int = 200,
        ) -> list[tuple[int, int, int]]:

    if game is None:
        raise ValueError("Input game is not correct")

    board = game.board()

    missed_moves: list[tuple[int, int, int]] = [] # [move_number, ply, harm]

    with eval(engine_path=engine_path, depth=10) as ev:
        for move in game.mainline_moves():
            mover = board.turn
            if mover == target:
                best_move = ev.get_best_move(board)
                board.push(best_move)
                cp_best_move = ev.eval_cp(board)

                board.pop()
                board.push(move)
                cp_chosen_move = ev.eval_cp(board)

                delta = cp_best_move - cp_chosen_move
                missed_move = delta if mover == chess.WHITE else -delta

                if missed_move >= loss_threshold_cp:
                    missed_moves.append((int(board.fullmove_number), int(board.ply()), int(missed_move)))

            else:
                board.push(move)


    return missed_moves



if __name__ == "__main__":
    pgn_path_blunder = Path("tests/fixtures/blunder.pgn")
    pgn_path_missed = Path("tests/fixtures/missed_move.pgn")

    with open(pgn_path_blunder) as pgn:
        game_blunder = chess.pgn.read_game(pgn)

    with open(pgn_path_missed) as pgn:
        game_missed = chess.pgn.read_game(pgn)

    blunders = detect_blunders(game=game_blunder, eval= StockfishEvaluator, target=chess.WHITE)
    missed_moves = detect_missed_moves(game=game_missed, eval= StockfishEvaluator, target=chess.WHITE)
