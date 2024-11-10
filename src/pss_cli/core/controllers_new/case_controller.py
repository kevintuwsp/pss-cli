import os
import pathlib
import shutil
from typing import List
from pydantic import BaseModel

import PyQt5.QtWidgets as QtWidgets
from PyQt5.QtCore import pyqtSlot


from pss_cli.core.config import SCENARIO_PATH
from pss_cli.core.controllers_new import Controller
from pss_cli.core.models import Case, Scenario, ScenarioCaseLink
from pss_cli.utils.hash import get_hash
from pss_cli.core.database import db, Database
from pss_cli.core.logging import logger
from pss_cli.core.extractors import (
    BusDefinitionObjExtractor,
    BranchDefinitionObjExtractor,
    MachineDefinitionObjExtractor,
    TwoWindingTransformerDefinitionObjExtractor,
)


class CaseController(Controller):
    """Manages the cases in the project"""

    def __init__(self, view: QtWidgets.QWidget, db_model: Database = db) -> None:
        super().__init__(view, db_model)

    def add(
        self,
        name: str,
        description: str,
        file_path: str,
        scenario_names: List[str],
    ):
        """Add a case to the database"""

        md5_hash = get_hash(file_path)
        case = Case(
            name=name,
            description=description,
            file_path=file_path,
            md5_hash=md5_hash,
        )

        objects = []
        objects.append(case)
        scenarios = db.get_objects(
            Scenario,
            conditions=[Scenario.name.in_(scenario_names)],  # type: ignore
        )
        for scenario in scenarios:
            scenario_file_path = self.create_scenario_file(scenario, case)  # type: ignore
            scenario_case_link = ScenarioCaseLink(
                scenario=scenario,
                case=case,
                file_path=str(scenario_file_path),
                md5_hash=get_hash(str(scenario_file_path)),
            )
            objects.append(scenario_case_link)

        db.add_all_objects(objects, persist=True)
        db.refresh(case)

        bus_definitions = BusDefinitionObjExtractor().extract(case)
        branch_definitions = BranchDefinitionObjExtractor().extract(case)
        machine_definitions = MachineDefinitionObjExtractor().extract(case)
        two_winding_transformer_definitions = (
            TwoWindingTransformerDefinitionObjExtractor().extract(case)
        )

        db.add_all_objects(bus_definitions, commit=False, persist=True)
        db.add_all_objects(branch_definitions, commit=False, persist=True)
        db.add_all_objects(machine_definitions, commit=False, persist=True)
        db.add_all_objects(
            two_winding_transformer_definitions, commit=True, persist=True
        )

        db.commit()
        logger.info(f"Added case to the database: {case.name}")

    def delete(self, name: str):
        """Delete a case from the database"""

        case = db.get_object(Case, conditions=[Case.name == name])

        if case is None:
            logger.error(f"Case with name {name} does not exist")
            return

        self.remove_scenario_files(case)  # type: ignore
        db.delete_object(case)

    def remove_scenario_files(self, case: Case):
        """Remove the scenario files from the case"""

        scenario_case_links = db.get_objects(
            ScenarioCaseLink, conditions=[ScenarioCaseLink.case_id == case.id]
        )

        for scenario_case_link in scenario_case_links:
            if not scenario_case_link:
                continue
            if os.path.exists(scenario_case_link.file_path):
                os.remove(scenario_case_link.file_path)

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


class CaseModel(BaseModel):
    """Model for the case"""

    def __init__(self, db: Database = db):
        self.db = db

    @pyqtSlot(List[str])
    def get_case_names(self):
        """Get names of all cases"""

        cases = self.db.get_objects(Case)
        return [case.name for case in cases]  # type: ignore
