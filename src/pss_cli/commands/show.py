import typer
from typing import Optional
from typing_extensions import Annotated

from pss_cli.core.database import db
from pss_cli.core.prompts import prompt_table_names
from pss_cli.core.ui import print_models
from pss_cli.core.logging import log


app = typer.Typer()


@app.command(name="table")
def get_table(name: Annotated[Optional[str], typer.Argument()] = None):
    """Show table from database"""

    if not name:
        name = prompt_table_names()

    results = db.select_table(name)

    if not results:
        log.error(f"Table '{name}' not found in the database")
        return

    print_models(results)
    # for result in results:
    #     print_model(result)
