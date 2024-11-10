import PyQt5.QtWidgets as QtWidgets
from pydantic import BaseModel

from pss_cli.core.database import db, Database
from pss_cli.core.controllers_new import (
    Controller,
    CaseController,
    ScenarioController,
    # GeneratorController,
    GeneratingSystemController,
    # GeneratingSystemSetpointController,
)


class ControllerFactory(BaseModel):
    """Factory class for creating controllers"""

    def __init__(self):
        super().__init__()

    def create_controller(
        self,
        view: QtWidgets.QWidget,
        controller_name: str,
        db_model: Database = db,
    ) -> Controller:
        """Create a controller"""

        if controller_name == "case":
            return CaseController(view, db_model)
        elif controller_name == "scenario":
            return ScenarioController(view, db_model)
        # elif controller_name == "generator":
        #     return GeneratorController(view, db_model)
        elif controller_name == "generating_system":
            return GeneratingSystemController(view, db_model)
        # elif controller_name == "generating_system_setpoint":
        #     return GeneratingSystemSetpointController(view, db_model)
        else:
            raise ValueError(f"Controller {controller_name} not found")
