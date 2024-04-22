from sqlmodel import SQLModel, and_
import typer

from abc import ABC, abstractmethod
from typing import Sequence, Type
from rich import print
from pss_cli.core.extract_data import (
    extract_case_branch_data,
    extract_case_bus_data,
    extract_scenario_bus_values,
    extract_scenario_branch_values,
)
from pss_cli.core.database import db
from pss_cli.core.models import (
    Case,
    CaseBusData,
    CaseBranchData,
    Scenario,
    ScenarioBusValues,
    ScenarioBranchValues,
    ScenarioCaseLink,
)

app = typer.Typer()


class ScenarioValuesObjExtractor(ABC):
    @abstractmethod
    def extract_data_objs(
        self, scenario_case_link: ScenarioCaseLink
    ) -> Sequence[SQLModel]:
        raise NotImplementedError


class ScenarioValuesObjExtractorFactory:
    @staticmethod
    def create_extractor(
        extractor_type: Type[ScenarioValuesObjExtractor],
    ) -> ScenarioValuesObjExtractor:
        return extractor_type()


class CaseDataObjExtractor(ABC):
    @abstractmethod
    def extract_data_objs(self, case: Case) -> Sequence[SQLModel]:
        raise NotImplementedError


class CaseDataObjExtractorFactory:
    @staticmethod
    def create_extractor(
        extractor_type: Type[CaseDataObjExtractor],
    ) -> CaseDataObjExtractor:
        return extractor_type()


class CaseBusDataObjExtractor(CaseDataObjExtractor):
    def extract_data_objs(self, case: Case) -> Sequence[CaseBusData]:
        """Create a list of CaseBusData object to add to the database"""

        bus_data = extract_case_bus_data(case.file_path)
        case_bus_data = [
            CaseBusData(
                case_id=case.id,
                bus_number=bus["bus_number"],
                bus_name=bus["bus_name"].strip(),
                bus_base_voltage=bus["bus_base_voltage"],
                bus_type=bus["bus_type"],
            )
            for bus in bus_data
        ]

        return case_bus_data


class CaseBranchDataObjExtractor(CaseDataObjExtractor):
    def extract_data_objs(self, case: Case) -> Sequence[CaseBranchData]:
        """Create a list of CaseBranchData object to add to the database"""

        branch_data = extract_case_branch_data(case.file_path)
        case_branch_data = [
            CaseBranchData(
                case_id=case.id,
                from_bus_number=branch["from_bus_number"],
                to_bus_number=branch["to_bus_number"],
                branch_id=branch["branch_id"].strip(),
                from_bus_name=branch["from_bus_name"].strip(),
                to_bus_name=branch["to_bus_name"].strip(),
            )
            for branch in branch_data
        ]

        return case_branch_data


class ScenarioBusValuesObjExtractor(ScenarioValuesObjExtractor):
    def extract_data_objs(
        self, scenario_case_link: ScenarioCaseLink
    ) -> Sequence[ScenarioBusValues]:
        """Create a list of ScenarioBusValues objects to add to the database"""

        # NOTE: probably need better error handling
        if not scenario_case_link:
            print("No database row found.")

        bus_values = extract_scenario_bus_values(scenario_case_link.file_path)  # type: ignore
        scenario_bus_values = [
            ScenarioBusValues(
                case_id=scenario_case_link.case.id,
                scenario_id=scenario_case_link.scenario.id,
                bus_number=bus["bus_number"],
                bus_voltage_pu=bus["bus_voltage_pu"],
                bus_voltage_kv=bus["bus_voltage_kv"],
                bus_voltage_angle_deg=bus["bus_voltage_angle_deg"],
            )
            for bus in bus_values
        ]

        return scenario_bus_values


class ScenarioBranchValuesObjExtractor(ScenarioValuesObjExtractor):
    def extract_data_objs(
        self, scenario_case_link: ScenarioCaseLink
    ) -> Sequence[ScenarioBranchValues]:
        """Create a list of ScenarioBranchValues objects to add to the database"""

        # NOTE: probably need better error handling
        if not scenario_case_link:
            print("No database row found.")

        branch_values = extract_scenario_branch_values(scenario_case_link.file_path)  # type: ignore
        scenario_branch_values = [
            ScenarioBranchValues(
                case_id=scenario_case_link.case.id,
                scenario_id=scenario_case_link.scenario.id,
                from_bus_number=branch["from_bus_number"],
                to_bus_number=branch["to_bus_number"],
                branch_id=branch["branch_id"].strip(),
                active_power_mw=branch["active_power_mw"],
                reactive_power_mw=branch["reactive_power_mw"],
            )
            for branch in branch_values
        ]

        return scenario_branch_values


@app.command("case-data")
def extract_case_data():
    """Extract case data and insert into database"""

    creators = [
        CaseBusDataObjExtractor,
        CaseBranchDataObjExtractor,
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
            for obj in CaseDataObjExtractorFactory.create_extractor(
                creator
            ).extract_data_objs(case)  # type: ignore
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
        ScenarioBusValuesObjExtractor,
        ScenarioBranchValuesObjExtractor,
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
            for obj in CaseDataObjExtractorFactory.create_extractor(
                creator
            ).extract_data_objs(
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
