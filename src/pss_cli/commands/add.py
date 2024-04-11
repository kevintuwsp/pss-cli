import typer

from sqlmodel import Session
from rich import print

from pss_cli.database import engine
from pss_cli.models import Scenario, Case
from pss_cli.prompts import prompt_case_path


app = typer.Typer()


@app.command("scenario")
def add_scenario(name: str, description: str = None):
    """Add a scenario to the database"""

    scenario = Scenario(name=name, description=description)

    with Session(engine) as session:
        session.add(scenario)
        session.commit()

    print("Added scenario to the database.")


@app.command("case")
def add_case(
    name: str, description: str = None, root_dir=".", match_pattern: str = "*.py"
):
    """Add a case to the database"""

    fpath = prompt_case_path(root_dir, match_pattern)

    if not fpath:
        print("No file selected.")
        return

    case = Case(
        name=name,
        file_name=str(fpath),
    )

    with Session(engine) as session:
        session.add(case)
        session.commit()
        session.refresh(case)

    print("Added case to the database:")
    print(case)
