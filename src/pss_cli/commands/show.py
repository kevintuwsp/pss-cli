import typer
from rich import print
from pss_cli.database import select_table
from typing import List


app = typer.Typer()


@app.command(name="table")
def get_table(table_name: List[str]):
    """Show table from database"""

    for item in table_name:
        results = select_table(item)
        print(results)
