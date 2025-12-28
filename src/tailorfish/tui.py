from rich import box
from rich.console import Console
from rich.table import Table

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


for rank in reversed(ranks):
    table.add_row(rank, *" "*8, rank)

table.add_row(*files)

console.print(table)
