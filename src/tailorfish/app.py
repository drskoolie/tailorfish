import chess
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Static


LIGHT_BG = "red"      # try "grey23" later
DARK_BG  = "gray10"

WHITE_FG = "yellow"
BLACK_FG = "bright_black"

def board_to_ascii(board: chess.Board) -> str:
    lines: list[str] = []
    lines.append("    a  b  c  d  e  f  g  h")
    lines.append("    ----------------------")

    for rank in range(7, -1, -1):
        row = [f"{rank+1}| "]
        for file in range(8):
            sq = chess.square(file, rank)
            piece = board.piece_at(sq)

            # a1 is dark -> (file+rank) % 2 == 0 gives dark on a1
            bg = DARK_BG if (file + rank) % 2 == 0 else LIGHT_BG

            if piece is None:
                # two spaces so the square has width
                row.append(f"[on {bg}]   [/]")
            else:
                sym = piece.symbol()
                fg = WHITE_FG if sym.isupper() else BLACK_FG
                # leading space makes alignment look like a cell
                row.append(f"[{fg} underline on {bg}] {sym} [/]")

        row.append(f" |{rank+1}")
        lines.append("".join(row))

    # File labels (no background needed, but you can add if you want)
    lines.append("    ______________________")
    lines.append("    a  b  c  d  e  f  g  h")
    return "\n".join(lines)



class TailorfishTUI(App):
    BINDINGS = [
            ("q", "quit", "Quit"),
            ]

    def __init__(self) -> None:
        super().__init__()
        self.board = chess.Board()

    def compose(self) -> ComposeResult:
        self.board_view = Static()
        yield self.board_view

    def on_mount(self) -> None:
        self.board_view.update(board_to_ascii(self.board))

    def action_quit(self) -> None:
        self.exit()

if __name__ == "__main__":
    from pathlib import Path

    from tailorfish.analysis import GameEvaluator, load_games_into_ram

    if False:
        pgn_path_drskoolie = Path("data/raw/lichess_drskoolie_2025-12-14.pgn")
        games = load_games_into_ram(pgn_path_drskoolie)

        ge = GameEvaluator()
        ge.load_game_directly(games[0]["game"], games[0]["target"])
        df = ge.move_analyzer()

    app = TailorfishTUI()
    app.run()
