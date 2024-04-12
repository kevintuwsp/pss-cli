import typer

from sqlmodel import Session
from rich import print

from pss_cli.database import engine, select_table
from pss_cli.models import Scenario, Case
from pss_cli.prompts import prompt_case_path, prompt_table
from pss_cli.ui import print_model


app = typer.Typer()


@app.command("scenario")
def add_scenario(name: str, description: str = None, link_all_cases: bool = False):
    """Add a scenario to the database"""

    scenario = Scenario(name=name, description=description)

    if link_all_cases:
        cases = select_table("case") 
    else:
        cases = prompt_table("case", parameter="name")

    scenario.cases = cases

    with Session(engine) as session:
        session.add(scenario)
        session.commit()
        session.refresh(scenario)

        print("Added scenario to the database.")
        print_model(scenario)
        for case in scenario.cases:
            print_model(case)


@app.command("case")
def add_case(
    name: str, description: str = None, root_dir=".", match_pattern: str = "*.sav"
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
        print_model(case)
