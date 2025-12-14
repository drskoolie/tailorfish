import chess
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Static

WHITE_COLOR = "yellow"
BLACK_COLOR = "bright_black"  # or "brown", "red", "orange1"

def board_to_ascii(board: chess.Board) -> str:
    lines: list[str] = []

    for rank in range(7, -1, -1):
        row: list[str] = []
        for file in range(8):
            sq = chess.square(file, rank)
            piece = board.piece_at(sq)

            if piece is None:
                row.append(".")
            else:
                sym = piece.symbol()
                if sym.isupper():
                    row.append(f"[{WHITE_COLOR}]{sym}[/{WHITE_COLOR}]")
                else:
                    row.append(f"[{BLACK_COLOR}]{sym}[/{BLACK_COLOR}]")

        lines.append(f"{rank+1}  " + " ".join(row))

    lines.append("")
    lines.append("   a b c d e f g h")
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
