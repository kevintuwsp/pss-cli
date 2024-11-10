import os
import pathlib
import shutil
from typing import List
import PyQt5.QtWidgets as QtWidgets

from pss_cli.core.config import SCENARIO_PATH
from pss_cli.core.controllers_new import Controller
from pss_cli.core.models import Case, Scenario, ScenarioCaseLink
from pss_cli.utils.hash import get_hash
from pss_cli.core.database import db, Database
from pss_cli.core.logging import logger


class ScenarioController(Controller):
    def __init__(self, view: QtWidgets.QWidget, db_model: Database = db):
        super().__init__(view, db_model)

    def add(self, name: str, description: str, case_names: List[str]) -> None:
        """Add a scenario to the database linked to the given cases"""

        scenario = Scenario(name=name, description=description)
        cases = self.db_model.get_objects(
            Case,
            conditions=[Case.name.in_(case_names)],  # type: ignore
        )

        if not cases:
            logger.error(f"No cases found with names {case_names}")
            return

        for case in cases:
            scenario_file_path = self._create_scenario_file(scenario, case)  # type: ignore
            scenario_case_link = ScenarioCaseLink(
                scenario=scenario,
                case=case,
                file_path=str(scenario_file_path),
                md5_hash=get_hash(str(scenario_file_path)),
            )
            self.db_model.add_object(scenario_case_link, commit=False, persist=True)
        logger.info(f"Added scenario {scenario.name} to the database")
        self.db_model.commit()

    def delete(self, name: str) -> None:
        """Delete a scenario from the database"""

        scenario = self.db_model.get_object(
            Scenario,
            conditions=[Scenario.name == name],
        )

        if not scenario:
            logger.error(f"Scenario {name} not found in the database")
            return

        scenario_case_links = self.db_model.get_objects(
            ScenarioCaseLink,
            conditions=[ScenarioCaseLink.scenario_id == scenario.id],
        )

        for scenario_case_link in scenario_case_links:
            if os.path.exists(scenario_case_link.file_path):  # type: ignore
                os.remove(scenario_case_link.file_path)  # type: ignore

        self.db_model.delete_object(scenario)
        logger.info(f"Deleted scenario from the database: {scenario.name}")

    def _create_scenario_file(self, scenario: Scenario, case: Case):
        """Create a file for the scenario"""

        case_file_path = pathlib.Path(case.file_path)
        scenario_file_path = self.get_scenario_file_path(scenario, case)
        os.makedirs(scenario_file_path.parent, exist_ok=True)
        shutil.copy(src=case_file_path, dst=scenario_file_path)

        return scenario_file_path

    def _get_scenario_filename(self, scenario: Scenario, case: Case) -> str:
        """Create a filename for the scenario"""

        case_file_path = pathlib.Path(case.file_path)
        extension = case_file_path.suffix
        return f"{case.name} - {scenario.name}{extension}"

    def _get_scenario_file_path(self, scenario: Scenario, case: Case) -> pathlib.Path:
        """Get the file path for the scenario"""

        directory = pathlib.Path(SCENARIO_PATH)
        file_name = self.get_scenario_filename(scenario, case)
        return directory.joinpath(file_name)
