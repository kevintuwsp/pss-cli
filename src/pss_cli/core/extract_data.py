from typing import Any, Dict, List
from pss_cli.psse.api.base import api
from pss_cli.utils.convert import get_list_of_dict


def extract_case_bus_data(fpath: str) -> List[Dict[str, Any]]:
    """Extract PSSE case data"""

    api.initialise()
    api.load_case(fpath)
    bus_info = api.subsystem_info("bus", ["NUMBER", "NAME", "BASE", "TYPE"])

    bus_info_dict = get_list_of_dict(
        keys=["bus_number", "bus_name", "bus_base_voltage", "bus_type"],
        list_of_tuples=bus_info,
    )
    return bus_info_dict


def extract_case_branch_data(fpath: str) -> List[Dict[str, Any]]:
    """Extract PSSE case branch data"""

    api.initialise()
    api.load_case(fpath)
    branch_info = api.subsystem_info(
        "brn", ["FROMNUMBER", "TONUMBER", "ID", "FROMNAME", "TONAME"]
    )

    branch_info_dict = get_list_of_dict(
        keys=[
            "from_bus_number",
            "to_bus_number",
            "branch_id",
            "from_bus_name",
            "to_bus_name",
        ],
        list_of_tuples=branch_info,
    )
    return branch_info_dict


def extract_scenario_bus_values(fpath: str) -> List[Dict[str, Any]]:
    """Extract PSSE case real bus values for the selected scenario"""

    api.initialise()
    api.load_case(fpath)
    bus_info = api.subsystem_info("bus", ["NUMBER", "PU", "KV", "ANGLED"])

    bus_info_dict = get_list_of_dict(
        keys=[
            "bus_number",
            "bus_voltage_pu",
            "bus_voltage_kv",
            "bus_voltage_angle_deg",
        ],
        list_of_tuples=bus_info,
    )
    return bus_info_dict


def extract_scenario_branch_values(fpath: str) -> List[Dict[str, Any]]:
    """Extract PSSE case real branch values for the selected scenario"""

    api.initialise()
    api.load_case(fpath)
    branch_info = api.subsystem_info("brn", ["FROMNUMBER", "TONUMBER", "ID", "P", "Q"])

    branch_info_dict = get_list_of_dict(
        keys=[
            "from_bus_number",
            "to_bus_number",
            "branch_id",
            "active_power_mw",
            "reactive_power_mw",
        ],
        list_of_tuples=branch_info,
    )
    return branch_info_dict
