import chess
from rich import box
from rich.console import Console
from rich.table import Table

def rank_row(board: chess.Board, rank: int):
    row = ""
    for file_idx in range(8):  # a → h
        square = chess.square(file_idx, rank)
        piece = board.piece_at(square)
        row += piece.symbol() if piece else " "
    return row


board = chess.Board()
rank_row(board, 0)



console = Console()
table = Table(
        title="Chess", 
        box=box.ROUNDED,
        show_lines=True,
        )


ranks = "12345678"
files = " ABCDEFGH "


for file in files:
    table.add_column(file)


for rank_no, rank in enumerate(reversed(ranks)):
    table.add_row(rank, *rank_row(board, rank_no), rank)

table.add_row(*files)

console.print(table)

