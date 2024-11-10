import os
import pathlib
import shutil
import PyQt5.QtWidgets as QtWidgets
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Sequence, Union
from pydantic import BaseModel
from sqlmodel import SQLModel
from pss_cli.core.database import db, Database
from pss_cli.core.models import Case, Scenario, ScenarioCaseLink
from pss_cli.core.config import SCENARIO_PATH


class Controller(ABC, BaseModel):
    """Base class for controllers"""

    def __init__(self, view: QtWidgets.QWidget, db_model: Database = db) -> None:
        self.view = view
        self.db_model = db_model

    @abstractmethod
    def add(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def delete(self, name: str) -> None:
        raise NotImplementedError

    def get_object(
        self,
        table_name: str,
        attribute: Optional[str],
        conditions: Optional[Dict[str, Union[str, int, float]]] = None,
    ) -> Union[str, Optional[SQLModel]]:
        """Get object from the database. If attribute is provided, return the attribute value."""

        table = self.db_model.get_table_object(table_name)
        if not table:
            raise ValueError(f"Table {table_name} not found")

        _conditions = None
        if conditions:
            _conditions = [
                getattr(table, key) == value for key, value in conditions.items()
            ]

        object = self.db_model.get_object(table, conditions=_conditions)
        if not object:
            raise ValueError(f"No object found in table {table_name}")

        if not attribute:
            return object

        return getattr(object, attribute)  # type: ignore

    def get_objects(
        self,
        table_name: str,
        attribute: Optional[str],
        conditions: Optional[Dict[str, Union[str, int, float]]] = None,
    ) -> Union[Sequence[str], Sequence[Optional[SQLModel]]]:
        """Get objects from the database. If attribute is provided, return a list of the attribute values."""

        table = self.db_model.get_table_object(table_name)
        if not table:
            raise ValueError(f"Table {table_name} not found")

        _conditions = None
        if conditions:
            _conditions = [
                getattr(table, key) == value for key, value in conditions.items()
            ]

        objects = db.get_objects(table, conditions=_conditions)
        if not objects:
            raise ValueError(f"No objects found in table {table_name}")

        if not attribute:
            return objects

        return [getattr(object, attribute) for object in objects]  # type: ignore

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
