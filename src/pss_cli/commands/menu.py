import typer

from pss_cli.prompts import prompt_table


app = typer.Typer()


@app.command()
def example(table_name: str):
    results = prompt_table(table_name, parameter="name")
