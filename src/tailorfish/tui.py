import chess
from rich import box
from rich.console import Console
from rich.table import Table
from rich.text import Text

class ChessTable():
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


board = chess.Board()

console = Console()

chess_table = ChessTable(board)

console.print(chess_table.make_table())
chess_table.board.push_san("e4")
console.print(chess_table.make_table())
chess_table.board.push_san("e5")
console.print(chess_table.make_table())
