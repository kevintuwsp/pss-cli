from typing import List, Tuple
from itertools import groupby
from operator import itemgetter
from pydantic import BaseModel

import psspy  # type: ignore

attr_type = itemgetter(0)


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

    def get_branch_ids(self) -> List[str]:
        """Return a list of branch ids"""

        ierr, branch_ids = psspy.abrnchar(string="ID")
        return branch_ids[0]

    def get_branch_from_bus_names(self) -> List[str]:
        """Return a list of branch from bus names"""

        ierr, branch_from_bus_names = psspy.abrnint(string="FROMNAME")
        return [x.strip() for x in branch_from_bus_names[0]]

    def get_branch_to_bus_names(self) -> List[str]:
        """Return a list of branch to bus names"""

        ierr, branch_to_bus_names = psspy.abrnint(string="TONAME")
        return [x.strip() for x in branch_to_bus_names[0]]

    def subsystem_info(
        self, name: str, attributes: List[str], sid: int = -1, inservice: bool = True
    ) -> List[Tuple]:
        """
        Returns requested attributes from the PSS(r)E subsystem API
        for the given subsystem id and subsystem element name.

        e.g. to retrieve bus attributes "NAME", "NUMBER" and "PU"

        subsystem_info('bus', ["NAME", "NUMBER", "PU"])

        where the 'bus' `name` argument comes from the original
        PSS(r)E subsystem API naming convention found in Chapter 8 of the
        PSS(r)E API.

        abusint  # bus
        amachint # mach
        aloadint # load
        abrnint  # branch

        Args:
        inservice [optional]: True (default) to list only information
            for in service elements;
        sid [optional]: list only information for elements in this
            subsystem id (-1, all elements by default).

        """
        name = name.lower()
        gettypes = getattr(psspy, "a%stypes" % name)
        apilookup = {
            "I": getattr(psspy, "a%sint" % name),
            "R": getattr(psspy, "a%sreal" % name),
            "X": getattr(psspy, "a%scplx" % name),
            "C": getattr(psspy, "a%schar" % name),
        }

        result = []
        ierr, attr_types = gettypes(attributes)

        for k, group in groupby(zip(attr_types, attributes), key=attr_type):
            func = apilookup[k]
            strings = list(zip(*group))[1]
            ierr, res = func(sid, flag=1 if inservice else 2, string=strings)
            result.extend(res)

        return list(zip(*result))
