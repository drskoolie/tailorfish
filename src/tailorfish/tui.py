import chess
from rich import box
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text


class ChessTable:
    def __init__(self, board: chess.Board):
        self.board = board

        self.files = " ABCDEFGH "

    def make_table(self) -> Table:
        table = Table(
                title="Chess", 
                box=box.ROUNDED,
                show_lines=True,
                )

        for file in self.files:
            table.add_column(file, justify="center", no_wrap=True)


        for rank_idx in range(7, -1, -1):
            label = str(rank_idx + 1)
            files = self.get_square_rank(rank_idx)
            table.add_row(label, *files, label)

        table.add_row(*self.files)

        return table


    def get_square_cell(self, file_idx: int, rank_idx: int) -> Text:
        sq = chess.square(file_idx, rank_idx)
            

        piece = self.board.piece_at(sq)
        glyph = piece.symbol() if piece else " "

        style =""
        white_style = "on blue bold white"
        black_style = "on magenta bold white"

        if piece:
            style = white_style if piece.color else black_style

        if self.board.move_stack:
            m = self.board.peek()

            if sq in [m.from_square, m.to_square]:
                style = "on red3 bold white"

        # light = (file_idx + rank_idx) % 2 == 0

        return Text(f" {glyph} ", style=style)

    def get_square_rank(self, rank_idx: int) -> list[Text]:
        files = []

        for file in range(0,8):
            files.append(self.get_square_cell(file, rank_idx))

        return files

def render(board: chess.Board) -> Panel:
    table = ChessTable(board).make_table()
    status = []
    status.append(f"Turn: {'White' if board.turn else 'Black'}")
    if board.is_check():
        status.append("CHECK!")
    if board.is_checkmate():
        status.append("CHECKMATE")
    elif board.is_stalemate():
        status.append("STALEMATE")

    help_line = "Enter SAN (e4, Nf3, O-O) or UCI (e2e4). Commands: undo, moves, fen, quit"
    body = f"[dim]{' | '.join(status)}[/dim]\n[dim]{help_line}[/dim]"
    return Panel.fit(table, subtitle=body)


def try_push_move(board: chess.Board, s: str) -> None:
    s = s.strip()

    # Try SAN first (what humans usually type)
    try:
        board.push_san(s)
        return
    except ValueError:
        pass

    # Then try UCI (e2e4, g1f3, etc.)
    try:
        mv = chess.Move.from_uci(s)
        if mv in board.legal_moves:
            board.push(mv)
            return
    except ValueError:
        pass

    raise ValueError("Invalid move (not legal SAN or UCI).")


def main() -> None:
    console = Console()
    board = chess.Board()

    with Live(render(board), console=console, refresh_per_second=1, screen=False) as live:
        while True:
            # refresh after each action (and after move input)
            live.update(render(board))

            try:
                s = console.input("[bold cyan]move>[/] ").strip()
            except (EOFError, KeyboardInterrupt):
                break

            if not s:
                continue

            cmd = s.lower()
            if cmd in {"q", "quit", "exit"}:
                break
            if cmd == "undo":
                if board.move_stack:
                    board.pop()
                continue
            if cmd == "fen":
                console.print(board.fen())
                continue
            if cmd == "moves":
                console.print(list(board.legal_moves))
                continue

            try:
                try_push_move(board, s)
            except ValueError as e:
                console.print(f"[bold red]{e}[/]")

            # stop if game over (optional)
            if board.is_game_over():
                live.update(render(board))
                console.print(f"[bold yellow]Game over:[/] {board.result()} ({board.outcome()})")
                break


if __name__ == "__main__":
    main()

