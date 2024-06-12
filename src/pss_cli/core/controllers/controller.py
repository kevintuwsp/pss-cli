from abc import ABC, abstractmethod
from pydantic import BaseModel

from pss_cli.core.controllers import (
    CaseController,
    ScenarioController,
    GeneratorController,
    GeneratingSystemController,
    GeneratingSystemSetpointController,
)


class Controller(ABC, BaseModel):
    """Base class for controllers"""

    @abstractmethod
    def add(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def delete(self, name: str) -> None:
        raise NotImplementedError


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
