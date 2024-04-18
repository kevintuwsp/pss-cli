from typing import List
from pydantic import BaseModel
from pss_cli.psse.api.base import PsseAPI


class Bus(BaseModel):
    number: int
    name: str
    type: int
    base_voltage: float


class Branch(BaseModel):
    from_bus_number: int
    to_bus_number: int
    branch_id: str
    from_bus_name: str
    to_bus_name: str


def get_case_bus_data(fpath: str) -> List[Bus]:
    """Load bus data from a PSSE Case"""

    api = PsseAPI()
    api.load_case(fpath)
    bus_numbers = api.get_bus_numbers()
    bus_names = api.get_bus_names()
    bus_types = api.get_bus_types()
    bus_base_voltages = api.get_bus_base_voltages()

    return [
        Bus(*x) for x in zip([bus_numbers, bus_names, bus_types, bus_base_voltages])
    ]


def get_case_branch_data(fpath: str) -> List[Branch]:
    """Load branch data from a PSSE Case"""

    api = PsseAPI()
    api.load_case(fpath)
    from_bus_numbers = api.get_branch_from_numbers()
    to_bus_numbers = api.get_branch_to_numbers()
    branch_ids = api.get_branch_ids()
    from_bus_names = api.get_branch_from_bus_names()
    to_bus_names = api.get_branch_to_bus_names()

    return [
        Branch(*x).dict()
        for x in zip(
            [from_bus_numbers, to_bus_numbers, branch_ids, from_bus_names, to_bus_names]
        )
    ]
