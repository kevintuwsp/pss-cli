import typer
from rich import print
from pss_cli.database import select_table, get_all_table_names
from typing import Optional

from pss_cli.prompts import prompt_table_names
from pss_cli.ui import print_model


app = typer.Typer()


@app.command(name="table")
def get_table(name: Optional[str] = None):
    """Show table from database"""

    if not name:
        name = prompt_table_names()

    results = select_table(name)
    for result in results:
        print_model(result)
