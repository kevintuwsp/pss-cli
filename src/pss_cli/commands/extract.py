from sqlmodel import SQLModel, and_
import typer

from abc import ABC, abstractmethod
from typing import Sequence, Type
from rich import print
from pss_cli.psse.funcs.extract import (
    extract_bus_definitions,
    extract_branch_definitions,
    extract_machine_definitions,
    extract_bus_values,
    extract_branch_values,
    extract_machine_values,
)
from pss_cli.core.database import db
from pss_cli.core.models import (
    Case,
    BusDefinition,
    BranchDefinition,
    MachineDefinition,
    BusValues,
    BranchValues,
    MachineValues,
    ScenarioCaseLink,
)

app = typer.Typer()


class ValuesObjExtractor(ABC):
    @abstractmethod
    def extract(
        self, scenario_case_link: ScenarioCaseLink, refresh: bool = True
    ) -> Sequence[SQLModel]:
        raise NotImplementedError


class ValuesObjExtractorFactory:
    @staticmethod
    def create_extractor(
        extractor_type: Type[ValuesObjExtractor],
    ) -> ValuesObjExtractor:
        return extractor_type()


class DefinitionObjExtractor(ABC):
    @abstractmethod
    def extract(self, case: Case, refresh: bool = True) -> Sequence[SQLModel]:
        raise NotImplementedError


class DefinitionObjExtractorFactory:
    @staticmethod
    def create_extractor(
        extractor_type: Type[DefinitionObjExtractor],
    ) -> DefinitionObjExtractor:
        return extractor_type()


class BusDefinitionObjExtractor(DefinitionObjExtractor):
    def extract(self, case: Case, refresh: bool = True) -> Sequence[BusDefinition]:
        """Create a list of BusDefintion objects to add to the database"""

        busses = extract_bus_definitions(case.file_path)
        objs = [
            BusDefinition(
                case_id=case.id,
                bus_number=bus["bus_number"],
                bus_name=bus["bus_name"].strip(),
                bus_base_voltage=bus["bus_base_voltage"],
                bus_type=bus["bus_type"],
            )
            for bus in busses
        ]

        return objs


class BranchDefinitionObjExtractor(DefinitionObjExtractor):
    def extract(self, case: Case, refresh: bool = True) -> Sequence[BranchDefinition]:
        """Create a list of BranchDefintion objects to add to the database"""

        branches = extract_branch_definitions(case.file_path)
        objs = [
            BranchDefinition(
                case_id=case.id,
                from_bus_number=branch["from_bus_number"],
                to_bus_number=branch["to_bus_number"],
                branch_id=branch["branch_id"].strip(),
                from_bus_name=branch["from_bus_name"].strip(),
                to_bus_name=branch["to_bus_name"].strip(),
            )
            for branch in branches
        ]

        return objs


class MachineDefinitionObjExtractor(DefinitionObjExtractor):
    def extract(self, case: Case, refresh: bool = True) -> Sequence[MachineDefinition]:
        """Create a list of MachineDefintion objects to add to the database"""

        machines = extract_machine_definitions(case.file_path)
        objs = [
            MachineDefinition(
                case_id=case.id,
                bus_number=machine["bus_number"],
                machine_name=machine["machine_name"],
                machine_id=machine["machine_id"].strip(),
            )
            for machine in machines
        ]

        return objs


class BusValuesObjExtractor(ValuesObjExtractor):
    def extract(
        self, scenario_case_link: ScenarioCaseLink, refresh: bool = True
    ) -> Sequence[BusValues]:
        """Create a list of ScenarioBusValues objects to add to the database"""

        # NOTE: probably need better error handling
        if not scenario_case_link:
            print("No database row found.")

        bus_values = extract_bus_values(scenario_case_link.file_path)  # type: ignore
        objs = [
            BusValues(
                case_id=scenario_case_link.case.id,
                scenario_id=scenario_case_link.scenario.id,
                bus_number=bus["bus_number"],
                bus_voltage_pu=bus["bus_voltage_pu"],
                bus_voltage_kv=bus["bus_voltage_kv"],
                bus_voltage_angle_deg=bus["bus_voltage_angle_deg"],
            )
            for bus in bus_values
        ]

        return objs


class BranchValuesObjExtractor(ValuesObjExtractor):
    def extract(
        self, scenario_case_link: ScenarioCaseLink, refresh: bool = True
    ) -> Sequence[BranchValues]:
        """Create a list of ScenarioBranchValues objects to add to the database"""

        # NOTE: probably need better error handling
        if not scenario_case_link:
            print("No database row found.")

        branch_values = extract_branch_values(scenario_case_link.file_path)  # type: ignore
        objs = [
            BranchValues(
                case_id=scenario_case_link.case.id,
                scenario_id=scenario_case_link.scenario.id,
                from_bus_number=branch["from_bus_number"],
                to_bus_number=branch["to_bus_number"],
                branch_id=branch["branch_id"].strip(),
                active_power_mw=branch["active_power_mw"],
                reactive_power_mvar=branch["reactive_power_mvar"],
            )
            for branch in branch_values
        ]

        return objs


class MachineValuesObjExtractor(ValuesObjExtractor):
    def extract(
        self, scenario_case_link: ScenarioCaseLink, refresh: bool = True
    ) -> Sequence[MachineValues]:
        """Create a list of MachineValues objects to add to the database"""

        # NOTE: probably need better error handling
        if not scenario_case_link:
            print("No database row found.")

        machine_values = extract_machine_values(scenario_case_link.file_path)  # type: ignore
        objs = [
            MachineValues(
                case_id=scenario_case_link.case.id,
                scenario_id=scenario_case_link.scenario.id,
                bus_number=machine["bus_number"],
                machine_id=machine["machine_id"].strip(),
                mbase_mva=machine["mbase_mva"],
                active_power_mw=machine["active_power_mw"],
                reactive_power_mvar=machine["reactive_power_mvar"],
                pmax=machine["pmax"],
                pmin=machine["pmin"],
                qmax=machine["qmax"],
                qmin=machine["qmin"],
            )
            for machine in machine_values
        ]

        return objs


@app.command("case-data")
def extract_case_data():
    """Extract case data and insert into database"""

    # TODO: Probably ask the factory for all extractor objects
    creators = [
        BusDefinitionObjExtractor,
        BranchDefinitionObjExtractor,
        MachineDefinitionObjExtractor,
    ]
    cases = db.select_table("case")

    if not cases:
        print("No cases found in the database.")
        return

    try:
        objs = [
            obj
            for case in cases
            for creator in creators
            for obj in DefinitionObjExtractorFactory.create_extractor(creator).extract(
                case  # type: ignore
            )
        ]

    except Exception as e:
        print(f"An error occurred while extracting data: {e}")
        return

    with db.session() as session:
        try:
            for obj in objs:
                session.add(obj)
            session.commit()
        except Exception as e:
            print(f"An error occurred while inserting data into the database: {e}")

    print(f"[green]Added {len(objs)} rows to the database.[/green]")


@app.command("scenario-data")
def extract_scenario_data():
    """Extract scenario data and insert into database"""

    creators = [
        BusValuesObjExtractor,
        BranchValuesObjExtractor,
        MachineValuesObjExtractor,
    ]
    session = db.session()
    scenarios_case_links = db.select_table("scenariocaselink", session=session)

    if not scenarios_case_links:
        print("No scenario cases found in the database.")
        return

    # TODO: seems like a lot of steps, refactor to smaller functions, introduce facade pattern
    # TODO: need to delete existing data, or only refresh if the hash is different

    try:
        objs = [
            obj
            for scenario_case_link in scenarios_case_links
            for creator in creators
            for obj in ValuesObjExtractorFactory.create_extractor(creator).extract(
                scenario_case_link,  # type: ignore
            )  # type: ignore
        ]
        session.close()

        for obj in objs:
            session.add(obj)
        session.commit()

    except Exception as e:
        print(f"An error occurred while extracting data: {e}")
        return

    print(f"[green]Added {len(objs)} rows to the database.[/green]")
