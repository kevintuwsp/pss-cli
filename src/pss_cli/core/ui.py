from typing import List, Sequence, Union
from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from sqlmodel import SQLModel

from pss_cli.core.logging import log


def print_model(
    model: SQLModel,
    key_color: str = "sky_blue3",
    value_color: str = "grey66",
):
    """Print out model parameters"""

    key_values = []
    for key in model.__table__.columns.keys():
        value = model.__getattribute__(key)
        key_values.append(
            f"[{key_color}]{key}[/{key_color}]=[{value_color}]{value}[/{value_color}]"
        )

    title = model.__tablename__
    print(Panel(" | ".join(key_values), expand=False, title=title))


def print_models(models: Sequence[Union[SQLModel, None]]):
    """Print out model parameters"""

    console = Console()
    if models[0] is None:
        console.print("No results to show.")

    table = Table(title=models[0].__tablename__, show_lines=False)  # type: ignore

    columns = models[0].model_dump().keys()  # type: ignore
    for column in columns:
        table.add_column(column)

    for model in models:
        values = [str(x) for x in model.model_dump().values()]  # type: ignore
        table.add_row(*values)

    console.print(table)
