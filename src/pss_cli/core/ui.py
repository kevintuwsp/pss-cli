from rich.panel import Panel
from sqlmodel import SQLModel

from pss_cli.core.logging import log


def print_model(
    model: SQLModel, key_color: str = "sky_blue3", value_color: str = "grey66"
):
    """Print out model parameters"""

    key_values = []
    for key in model.__table__.columns.keys():
        value = model.__getattribute__(key)
        key_values.append(
            f"[{key_color}]{key}[/{key_color}]=[{value_color}]{value}[/{value_color}]"
        )

    title = model.__tablename__
    log.info(Panel(" | ".join(key_values), expand=False, title=title))
