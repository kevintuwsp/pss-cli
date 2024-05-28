import typer

from rich.traceback import install

from pss_cli.core.database import db
from pss_cli.commands import add, show, extract, gui


install(show_locals=True)

app = typer.Typer()
app.add_typer(add.app, name="add")
app.add_typer(show.app, name="show")
app.add_typer(extract.app, name="extract")
app.add_typer(gui.app, name="gui")


def main():
    db.create_db_and_tables()
    app()
