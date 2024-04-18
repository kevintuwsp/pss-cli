import typing
from typing import List
from pydantic import BaseModel

if typing.TYPE_CHECKING:
    import psspy  # type: ignore


class PsseCaseDataMixin(BaseModel):
    def get_bus_numbers(self) -> List[int]:
        """Return a list of all bus numbers in the case"""

        ierr, bus_numbers = psspy.abusint(string="NUMBER")
        return bus_numbers[0]

    def get_bus_names(self) -> List[int]:
        """Return a list of bus names in the case"""

        ierr, bus_names = psspy.abuschar(string="NAME")
        return [x.strip() for x in bus_names[0]]

    def get_bus_types(self) -> List[int]:
        """Return a list of bus types in the case"""

        ierr, bus_types = psspy.abusint(string="TYPE")
        return bus_types[0]

    def get_bus_base_voltages(self) -> List[float]:
        """Return a list of bus base voltages in kV"""

        ierr, bus_base_voltages = psspy.abusreal(string="BASE")
        return bus_base_voltages

    def get_branch_from_numbers(self) -> List[int]:
        """Return a list of branch from numbers"""

        ierr, branch_from_numbers = psspy.abrnint(string="FROMNUMBER")
        return branch_from_numbers[0]

    def get_branch_to_numbers(self) -> List[int]:
        """Return a list of branch to numbers"""

        ierr, branch_to_numbers = psspy.abrnint(string="TONUMBER")
        return branch_to_numbers[0]

    def get_branch_from_bus_names(self) -> List[str]:
        """Return a list of branch from bus names"""

        ierr, branch_from_bus_names = psspy.abrnint(string="FROMNAME")
        return [x.strip() for x in branch_from_bus_names[0]]

    def get_branch_to_bus_names(self) -> List[str]:
        """Return a list of branch to bus names"""

        ierr, branch_to_bus_names = psspy.abrnint(string="TONAME")
        return [x.strip() for x in branch_to_bus_names[0]]
