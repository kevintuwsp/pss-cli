import typer

from rich.traceback import install

from pss_cli.core.database import db
from pss_cli.commands import add, show, menu, extract


install(show_locals=True)

app = typer.Typer()
app.add_typer(add.app, name="add")
app.add_typer(show.app, name="show")
app.add_typer(menu.app, name="menu")
app.add_typer(extract.app, name="extract")


def main():
    db.create_db_and_tables()
    app()
