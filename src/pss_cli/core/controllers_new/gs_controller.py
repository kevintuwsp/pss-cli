import PyQt5.QtWidgets as QtWidgets
from typing import List

from pss_cli.core.controllers_new import Controller
from pss_cli.core.models import Case, Scenario, ScenarioCaseLink
from pss_cli.utils.hash import get_hash
from pss_cli.core.database import db, Database
from pss_cli.core.logging import logger


class GeneratingSystemController(Controller):
    """Manages the generating systems in the project"""

    def __init__(self, view: QtWidgets.QWidget, db_model: Database = db):
        super().__init__(view, db_model)

    def add(
        self, name: str, description: str, file_path: str, scenario_names: List[str]
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
        scenarios = self.db_model.get_objects(
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

        self.db_model.add_all_objects(objects, persist=True)
        self.db_model.refresh(case)

        self.db_model.commit()
        logger.info(f"Added case to the database: {case.name}")

    def delete(self, name: str):
        """Delete a case from the database"""

        case = self.db_model.get_object(Case, conditions=[Case.name == name])

        if case is None:
            logger.error(f"Case with name {name} does not exist")
            return

        self.remove_scenario_files(case)  # type: ignore
        self.db_model.delete_object(case)
