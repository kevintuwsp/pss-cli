import typer
import pathlib
import shutil
import os

from typing import Optional
from typing_extensions import Annotated
from sqlalchemy.exc import IntegrityError

from pss_cli.core.database import db
from pss_cli.core.models import (
    Scenario,
    Case,
    ScenarioCaseLink,
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
from pss_cli.core.ui import print_models, print_model
from pss_cli.utils.hash import get_hash
from pss_cli.core.config import SCENARIO_PATH
from pss_cli.core.logging import log


app = typer.Typer()


@app.command("scenario")
def add_scenario(
    name: str, description: Optional[str] = None, link_all_cases: bool = False
):
    """Add a scenario to the database"""

    scenario = Scenario(name=name, description=description)

    if link_all_cases:
        cases = db.select_table("case")
    else:
        cases = prompt_table("case", parameter="name")

    directory = pathlib.Path(SCENARIO_PATH)
    os.makedirs(directory, exist_ok=True)

    scenario_case_links = []
    for case in cases:  # type: ignore
        case_file_path = pathlib.Path(case.file_path)  # type: ignore
        extension = case_file_path.suffix
        file_name = f"{case.name} - {scenario.name}{extension}"
        file_path = directory.joinpath(file_name)

        shutil.copy(src=case_file_path, dst=file_path)

        md5_hash = get_hash(str(file_path))
        scenario_case_link = ScenarioCaseLink(
            case=case,
            scenario=scenario,
            file_path=str(file_path),
            md5_hash=md5_hash,
        )
        scenario_case_links.append(scenario_case_link)

    # TODO: Refactor into small functions
    # TODO: Should populate the scenario values extraction tables here

    with db.session() as session:
        for obj in scenario_case_links:
            session.add(obj)
        session.commit()


@app.command("case")
def add_case(
    name: str,
    description: Optional[str] = None,
    root_dir=".",
    match_pattern: str = "*.sav",
):
    """Add a case to the database"""

    fpath = prompt_case_path(root_dir, match_pattern)

    if not fpath:
        log.error("No file selected.")
        return

    md5_hash = get_hash(fpath)

    case = Case(
        name=name, description=description, file_path=str(fpath), md5_hash=md5_hash
    )
    # TODO: Should populate the data extraction tables here

    with db.session() as session:
        db.add(case, session=session, commit=True)

        log.info("Added case to the database:")
        print_model(case)


@app.command("gs")
def add_generating_system(name: str):
    """Add a generating system to the case"""

    case = prompt_select_table("case", parameters=None)

    branch = prompt_select_table(
        "branchdefinition", parameters=["from_bus_number", "to_bus_number", "branch_id"]
    )
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
        db.add(generating_system, session=session, commit=True)
        print_model(generating_system)


@app.command("generator")
def add_generator():
    """Add a generator to the case"""

    generating_system = prompt_select_table("generatingsystem", parameters=["name"])
    machine = prompt_select_table(
        "machinedefinition", parameters=["machine_name", "bus_number", "machine_id"]
    )
    generator = Generator(
        bus_number=machine.bus_number,
        machine_id=str(machine.machine_id),
        generating_system_id=generating_system.id,
    )

    with db.session() as session:
        db.add(generator, session=session, commit=True)
        print_model(generator)


@app.command("setpoint")
def add_setpoint(
    p_setpoint: Annotated[Optional[float], typer.Option()] = None,
    q_setpoint: Annotated[Optional[float], typer.Option()] = None,
):
    """Add a P and/or Q setpoint to a generating system"""

    if not (p_setpoint or q_setpoint):
        log.error("Please provide either a P setpoint or Q setpoint")
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
            db.add(gs_setpoint, session=session, commit=True)

        except IntegrityError as e:
            log.error(
                "The generating system already has an existing setpoint for this scenario"
            )
            log.error(e)
            session.rollback()
            return

        print_model(gs_setpoint)
