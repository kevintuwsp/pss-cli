import typing
from pydantic import BaseModel

if typing.TYPE_CHECKING:
    from pss_cli.core.controllers import (
        Controller,
        CaseController,
        ScenarioController,
        GeneratorController,
        GeneratingSystemController,
        GeneratingSystemSetpointController,
    )


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
