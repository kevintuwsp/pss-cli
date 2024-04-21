import typer

from typing import Optional
from typing_extensions import Annotated
from rich import print
from sqlalchemy.exc import IntegrityError

from pss_cli.core.database import db
from pss_cli.core.models import (
    Scenario,
    Case,
    GeneratingSystem,
    GeneratingSystemSetpoint,
    Generator,
)

from pss_cli.core.prompts import (
    prompt_bool,
    prompt_case_path,
    prompt_table,
    prompt_select_table,
)
from pss_cli.core.ui import print_model
from pss_cli.utils.hash import get_hash


app = typer.Typer()


@app.command("scenario")
def add_scenario(name: str, description: str = None, link_all_cases: bool = False):
    """Add a scenario to the database"""

    scenario = Scenario(name=name, description=description)

    if link_all_cases:
        cases = db.select_table("case")
    else:
        cases = prompt_table("case", parameter="name")

    scenario.cases = cases
    # TODO: Need to create a new file (copy) and add to db via association table

    with db.session() as session:
        db.add(scenario, session=session)
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

    md5_hash = get_hash(fpath)

    case = Case(name=name, file_path=str(fpath), md5_hash=md5_hash)

    with db.session() as session:
        db.add(case, session=session)

        print("Added case to the database:")
        print_model(case)


@app.command("gs")
def add_generating_system(name: str):
    """Add a generating system to the case"""

    case = prompt_select_table("case", parameter=None)

    branch = prompt_select_table("casebranchdata", parameter="from_bus_number")
    reversed = prompt_bool(message="Reverse power flow direction?")
    from_bus = branch.from_bus_number
    to_bus = branch.to_bus_number

    generating_system = GeneratingSystem(
        name=name,
        from_bus=from_bus,
        to_bus=to_bus,
        case=case,
        reversed=reversed,
    )

    with db.session() as session:
        db.add(generating_system, session=session)
        print_model(generating_system)


@app.command("generator")
def add_generator(bus_number: int, machine_id: int):
    """Add a generator to the case"""

    generating_system = prompt_select_table("generatingsystem", parameter="name")
    generator = Generator(
        bus_number=bus_number,
        machine_id=str(machine_id),
        generating_systems=generating_system,
    )

    with db.session() as session:
        db.add(generator, session=session)
        print_model(generator)


@app.command("setpoint")
def add_setpoint(
    p_setpoint: Annotated[Optional[float], typer.Option()] = None,
    q_setpoint: Annotated[Optional[float], typer.Option()] = None,
):
    """Add a P and/or Q setpoint to a generating system"""

    if not (p_setpoint or q_setpoint):
        print("Please provide either a P setpoint or Q setpoint")
        return

    scenario = prompt_select_table("scenario", parameter="name")
    generating_system = prompt_select_table("generatingsystem", parameter="name")

    gs_setpoint = GeneratingSystemSetpoint(
        scenario_id=scenario.id,
        generating_system_id=generating_system.id,
        p_setpoint=p_setpoint,
        q_setpoint=q_setpoint,
    )

    with db.session() as session:
        try:
            db.add(gs_setpoint, session=session)

        except IntegrityError:
            print(
                "The generating system already has an existing setpoint for this scenario"
            )
            session.rollback()
            print_model(scenario)
            print_model(generating_system)
            return

        print_model(gs_setpoint)
