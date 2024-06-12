from abc import ABC, abstractmethod
import os
import pathlib
import shutil
from pydantic import BaseModel
from typing import List, Sequence, Optional

from sqlmodel import select

from pss_cli.core.database import db
from pss_cli.core.models import BranchDefinition, Case, Generator
from pss_cli.core.models import Scenario, ScenarioCaseLink
from pss_cli.core.config import SCENARIO_PATH
from pss_cli.utils.hash import get_hash
from pss_cli.core.logging import logger
from pss_cli.core.models import (
    BusDefinition,
    MachineDefinition,
    GeneratingSystem,
    GeneratingSystemSetpoint,
)
from pss_cli.core.extractors import (
    BusDefinitionObjExtractor,
    BranchDefinitionObjExtractor,
    MachineDefinitionObjExtractor,
    TwoWindingTransformerDefinitionObjExtractor,
)


class Controller(ABC, BaseModel):
    """Base class for controllers"""

    @abstractmethod
    def add(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def delete(self, *args, **kwargs):
        raise NotImplementedError

    def get_objects_from_db(self, table_name: str):
        """Return a list of objects from the database"""

        table_obj = db.get_table_object(table_name)
        with db.session() as session:
            statement = select(table_obj)
            objects = session.exec(statement).all()

        return objects

    def get_generating_systems(
        self,
        case: Case,
    ) -> Sequence[GeneratingSystem]:
        """Return a list of generating systems for a case"""

        with db.session() as session:
            statement = select(GeneratingSystem).where(
                GeneratingSystem.case_id == case.id
            )
            generating_systems = session.exec(statement).all()

        return generating_systems

    def get_scenario(self, name: str) -> Scenario:
        """Return a scenario"""

        with db.session() as session:
            statement = select(Scenario).where(Scenario.name == name)
            scenario = session.exec(statement).first()

        return scenario

    def get_scenarios(self, case_name: Optional[str] = None) -> Sequence[Scenario]:
        """Return a list of scenarios"""

        if case_name:
            case = self.get_case(case_name)

        with db.session() as session:
            statement = select(Scenario)
            if case_name:
                case = self.get_case(case_name)
                statement = statement.where(ScenarioCaseLink.case_id == case.id).where(
                    ScenarioCaseLink.scenario_id == Scenario.id
                )
            scenarios = session.exec(statement).all()

        return scenarios

    def get_cases(self) -> Sequence[Case]:
        """Return a list of cases"""

        with db.session() as session:
            statement = select(Case)
            cases = session.exec(statement).all()

        return cases

    def get_case(self, name: str) -> Case:
        with db.session() as session:
            statement = select(Case).where(Case.name == name)
            case = session.exec(statement).first()

        return case  # type: ignore

    def get_bus_name(self, case: Case, bus_no: int) -> Optional[str]:
        """Return the bus name for a bus number"""

        with db.session() as session:
            statement = (
                select(BusDefinition)
                .where(BusDefinition.case_id == case.id)
                .where(BusDefinition.bus_number == bus_no)
            )
            bus_def = session.exec(statement).first()

        if not bus_def:
            return None
        return bus_def.bus_name

    def get_generator_bus_numbers(self, case: Case) -> Sequence[int]:
        """Return a list of bus numbers for a case"""

        with db.session() as session:
            statement = select(MachineDefinition).where(
                MachineDefinition.case_id == case.id
            )
            machine_defs = session.exec(statement).all()

        return [machine_def.bus_number for machine_def in machine_defs]

    def get_machine_ids(self, bus_number: float, case: Case) -> Sequence[str]:
        """Return a list of machine IDs for a case"""

        with db.session() as session:
            statement = (
                select(MachineDefinition)
                .where(MachineDefinition.case_id == case.id)
                .where(MachineDefinition.bus_number == bus_number)
            )
            machine_defs = session.exec(statement).all()

        return [machine_def.machine_id for machine_def in machine_defs]

    def get_branch_ids(self, case: Case, from_bus_no: int, to_bus_no: int) -> List[str]:
        """Return a list of branch IDs for a case"""

        with db.session() as session:
            statement = (
                select(BranchDefinition)
                .where(BranchDefinition.case_id == case.id)
                .where(BranchDefinition.from_bus_number == from_bus_no)
                .where(BranchDefinition.to_bus_number == to_bus_no)
            )
            branch_definitions = session.exec(statement).all()

        return [branch_def.branch_id for branch_def in branch_definitions]

    def get_branch_to_bus_numbers(self, case: Case, from_bus_no: int) -> Sequence[int]:
        """Return a list of bus numbers for a case"""

        with db.session() as session:
            statement = (
                select(BranchDefinition)
                .where(BranchDefinition.case_id == case.id)
                .where(BranchDefinition.from_bus_number == from_bus_no)
            )
            branch_definitions = session.exec(statement).all()

        return [branch_def.to_bus_number for branch_def in branch_definitions]

    def get_branch_from_bus_numbers(self, case: Case) -> List[int]:
        """Return a list of bus numbers for a case"""

        with db.session() as session:
            statement = select(BranchDefinition).where(
                BranchDefinition.case_id == case.id
            )
            bus_definitions = session.exec(statement).all()

        return [bus_def.from_bus_number for bus_def in bus_definitions]

    def get_generating_system(
        self, name: str, case: Case
    ) -> Optional[GeneratingSystem]:
        """Return a generating system"""

        with db.session() as session:
            statement = (
                select(GeneratingSystem)
                .where(GeneratingSystem.name == name)
                .where(GeneratingSystem.case_id == case.id)
            )
            generating_system = session.exec(statement).first()

        return generating_system

    def get_files(self, root_dir: str, pattern="*.sav") -> List[pathlib.Path]:
        """Return a list of files in the root directory"""

        files = list(pathlib.Path(root_dir).rglob(pattern))
        return files

    def create_scenario_file(self, scenario: Scenario, case: Case):
        """Create a file for the scenario"""

        case_file_path = pathlib.Path(case.file_path)
        scenario_file_path = self.get_scenario_file_path(scenario, case)
        os.makedirs(scenario_file_path.parent, exist_ok=True)
        shutil.copy(src=case_file_path, dst=scenario_file_path)

        return scenario_file_path

    def get_scenario_filename(self, scenario: Scenario, case: Case) -> str:
        """Create a filename for the scenario"""

        case_file_path = pathlib.Path(case.file_path)
        extension = case_file_path.suffix
        return f"{case.name} - {scenario.name}{extension}"

    def get_scenario_file_path(self, scenario: Scenario, case: Case) -> pathlib.Path:
        """Get the file path for the scenario"""

        directory = pathlib.Path(SCENARIO_PATH)
        file_name = self.get_scenario_filename(scenario, case)
        return directory.joinpath(file_name)


class ScenarioController(Controller):
    def __init__(self):
        super().__init__()

    def add(self, name: str, description: str, cases: List[Case]) -> None:
        """Add a scenario to the database"""

        scenario = Scenario(name=name, description=description)

        with db.session() as session:
            for case in cases:
                scenario_file_path = self.create_scenario_file(scenario, case)
                scenario_case_link = ScenarioCaseLink(
                    scenario=scenario,
                    case=case,
                    file_path=str(scenario_file_path),
                    md5_hash=get_hash(str(scenario_file_path)),
                )
                db.add(scenario_case_link, session)
            logger.info(f"Added scenario {scenario.name} to the database")
            db.commit(session)

    def delete(self, scenario_name: str) -> None:
        """Delete a scenario from the database"""

        with db.session() as session:
            statement = select(Scenario).where(Scenario.name == scenario_name)
            scenario = session.exec(statement).first()

            if not scenario:
                logger.error(f"Scenario {scenario_name} not found in the database")
                return

            statement = select(ScenarioCaseLink).where(
                ScenarioCaseLink.scenario_id == scenario.id
            )
            scenario_case_links = session.exec(statement).all()

            for scenario_case_link in scenario_case_links:
                if os.path.exists(scenario_case_link.file_path):
                    os.remove(scenario_case_link.file_path)

            db.delete(scenario, session=session)
            logger.info(f"Deleted scenario from the database: {scenario.name}")


class CaseController(Controller):
    """Manages the cases in the project"""

    def __init__(self):
        super().__init__()

    def add(
        self, name: str, description: str, file_path: str, scenarios: List[Scenario]
    ):
        """Add a case to the database"""

        md5_hash = get_hash(file_path)
        with db.session() as session:
            case = Case(
                name=name,
                description=description,
                file_path=file_path,
                md5_hash=md5_hash,
            )

            for scenario in scenarios:
                scenario_file_path = self.create_scenario_file(scenario, case)
                scenario_case_link = ScenarioCaseLink(
                    scenario=scenario,
                    case=case,
                    file_path=str(scenario_file_path),
                    md5_hash=get_hash(str(scenario_file_path)),
                )
                session.add(scenario_case_link)
            session.add(case)
            session.commit()
            session.refresh(case)

            bus_definitions = BusDefinitionObjExtractor().extract(case)
            branch_definitions = BranchDefinitionObjExtractor().extract(case)
            machine_definitions = MachineDefinitionObjExtractor().extract(case)
            two_winding_transformer_definitions = (
                TwoWindingTransformerDefinitionObjExtractor().extract(case)
            )
            session.add_all(bus_definitions)
            session.add_all(branch_definitions)
            session.add_all(machine_definitions)
            session.add_all(two_winding_transformer_definitions)
            session.commit()

            logger.info(f"Added case to the database: {case.name}")

    def delete(self, name: str):
        """Delete a case from the database"""

        with db.session() as session:
            statement = select(Case).where(Case.name == name)
            case = session.exec(statement).first()
            if not case:
                logger.error(f"Case {name} not found in the database")
                return

            statement = select(ScenarioCaseLink).where(
                ScenarioCaseLink.case_id == case.id
            )
            scenario_case_links = session.exec(statement).all()

            for scenario_case_link in scenario_case_links:
                if os.path.exists(scenario_case_link.file_path):
                    os.remove(scenario_case_link.file_path)

            db.delete(case, session=session)
            logger.info(f"Deleted case from the database: {case}")


class GeneratorController(Controller):
    """Manages the generators in the project"""

    def __init__(self):
        super().__init__()

    def add(
        self,
        bus_number: int,
        machine_id: str,
        generating_system: GeneratingSystem,
    ) -> None:
        """Add a generator to the database"""

        generator = Generator(
            bus_number=bus_number,
            machine_id=machine_id,
            generating_system_id=generating_system.id,
        )

        with db.session() as session:
            session.add(generator)
            session.commit()
            logger.info(f"Added generator to the database: {bus_number} {machine_id}")

    def delete(self, bus_number: int, machine_id: str, gs_name: str):
        """Delete a generator from the database"""

        with db.session() as session:
            statement = select(GeneratingSystem).where(GeneratingSystem.name == gs_name)
            generating_system = session.exec(statement).first()

            if not generating_system:
                logger.error(f"Generating system {gs_name} not found in the database")
                return

            statement = (
                select(Generator)
                .where(Generator.bus_number == bus_number)
                .where(Generator.machine_id == machine_id)
                .where(Generator.generating_system_id == generating_system.id)
            )
            generator = session.exec(statement).first()
            session.delete(generator)
            session.commit()
            logger.info(
                f"Deleted generator from the database: {bus_number} {machine_id}"
            )


class GeneratingSystemController(Controller):
    """Manages the generating systems in the project"""

    def __init__(self):
        super().__init__()

    def add(
        self,
        name: str,
        case: Case,
        from_bus_no: int,
        to_bus_no: int,
        branch_id: str,
        reversed: bool,
    ):
        """Add a generating system to the database"""

        generating_system = GeneratingSystem(
            name=name,
            from_bus_number=from_bus_no,
            to_bus_number=to_bus_no,
            reversed=reversed,
            branch_id=branch_id,
            case_id=case.id,
        )

        with db.session() as session:
            session.add(generating_system)
            session.commit()
            logger.info(f"Added generating system to the database: {name}")

    def delete(self, name: str):
        """Delete a generating system from the database"""

        with db.session() as session:
            statement = select(GeneratingSystem).where(GeneratingSystem.name == name)
            generating_system = session.exec(statement).first()
            session.delete(generating_system)
            session.commit()
            logger.info(f"Deleted generating system from the database: {name}")


class GeneratingSystemSetpointController(Controller):
    """Manages the generating system setpoints in the project"""

    def __init__(self):
        super().__init__()

    def add(
        self,
        scenario_name: str,
        case_name: str,
        gs_name: str,
        p_setpoint: float,
        q_setpoint: float,
    ):
        """Add a generating system setpoint to the database"""

        with db.session() as session:
            statement = select(Scenario).where(Scenario.name == scenario_name)
            scenario = session.exec(statement).first()

            statement = select(Case).where(Case.name == case_name)
            case = session.exec(statement).first()

            statement = select(GeneratingSystem).where(GeneratingSystem.name == gs_name)
            generating_system = session.exec(statement).first()

            gs_setpoint = GeneratingSystemSetpoint(
                p_setpoint=p_setpoint,
                q_setpoint=q_setpoint,
                generating_system_id=generating_system.id,  # type: ignore
                scenario_id=scenario.id,  # type: ignore
                case_id=case.id,  # type: ignore
            )

            session.add(gs_setpoint)
            session.commit()
            logger.info("Added generating system setpoint to the database")

    def delete(self, gs_name: str, scenario_name: str) -> None:
        """Delete a generating system setpoint from the database"""

        with db.session() as session:
            statement = (
                select(GeneratingSystemSetpoint)
                .where(GeneratingSystem.name == gs_name)
                .where(Scenario.name == scenario_name)
            )
            generating_system_setpoints = session.exec(statement).all()
            for generating_system_setpoint in generating_system_setpoints:
                session.delete(generating_system_setpoint)
            session.commit()
            logger.info("Deleted generating system setpoints from the database")


class ControllerFactory(BaseModel):
    """Factory class for creating controllers"""

    def __init__(self):
        super().__init__()

    def create_controller(self, controller_name: str) -> Controller:
        """Create a controller"""

        if controller_name == "case":
            return CaseController()
        elif controller_name == "scenario":
            return ScenarioController()
        elif controller_name == "generator":
            return GeneratorController()
        elif controller_name == "generating_system":
            return GeneratingSystemController()
        elif controller_name == "generating_system_setpoint":
            return GeneratingSystemSetpointController()
        else:
            raise ValueError(f"Controller {controller_name} not found")
