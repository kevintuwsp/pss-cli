from typing import Any, Dict, List, Union
from pss_cli.psse.api.base import api
from pss_cli.utils.convert import get_list_of_dict


def extract_data(
    fpath: str, subsystem_type: str, subsystem_info_mapper: Dict[str, str]
) -> List[Dict[str, Any]]:
    """Extract PSSE case data and values, map return quantities to dictionary keys"""

    api.initialise()
    api.load_case(fpath)
    subsystem_info = api.subsystem_info(
        subsystem_type, list(subsystem_info_mapper.values())
    )
    subsystem_info_dict = get_list_of_dict(
        keys=list(subsystem_info_mapper.keys()),
        list_of_tuples=subsystem_info,
    )
    return subsystem_info_dict


def extract_bus_definitions(fpath: str) -> List[Dict[str, Any]]:
    """Extract PSSE case bus data"""

    info_dict = extract_data(
        fpath,
        subsystem_type="bus",
        subsystem_info_mapper={
            "bus_number": "NUMBER",
            "bus_name": "NAME",
            "bus_base_voltage": "BASE",
            "bus_type": "TYPE",
        },
    )
    return info_dict


def extract_branch_definitions(fpath: str) -> List[Dict[str, Any]]:
    """Extract PSSE case branch data"""

    info_dict = extract_data(
        fpath,
        subsystem_type="brn",
        subsystem_info_mapper={
            "from_bus_number": "FROMNUMBER",
            "to_bus_number": "TONUMBER",
            "branch_id": "ID",
            "from_bus_name": "FROMNAME",
            "to_bus_name": "TONAME",
            "pos_seq_impedance_pu": "RX",
            "zero_seq_impedance_pu": "RXZERO",
            "pos_seq_charging_capacitance_pu": "CHARGING",
            "zero_seq_charging_capacitance_pu": "CHARGINGZERO",
        },
    )
    return info_dict


def extract_machine_definitions(fpath: str) -> List[Dict[str, Any]]:
    """Extract PSSE case machine data"""

    info_dict = extract_data(
        fpath,
        subsystem_type="mach",
        subsystem_info_mapper={
            "bus_number": "NUMBER",
            "machine_id": "ID",
            "machine_name": "NAME",
        },
    )
    return info_dict


def extract_two_winding_transformer_definitions(fpath: str) -> List[Dict[str, Any]]:
    """Extract PSSE case two winding transformer data"""

    info_dict = extract_data(
        fpath,
        subsystem_type="trn",
        subsystem_info_mapper={
            "from_bus_number": "FROMNUMBER",
            "to_bus_number": "TONUMBER",
            "branch_id": "ID",
            "xfr_name": "XFRNAME",
            "pos_seq_impedance_pu": "RXNOM",
            "zero_seq_impedance_pu": "RXZERO",
            "vector_group": "VECTORGROUP",
            "controlled_bus_number": "ICONTNUMBER",
        },
    )

    return info_dict


def extract_three_winding_transformer_definitions(fpath: str) -> List[Dict[str, Any]]:
    """Extract PSSE case three winding transformer data"""

    info_dict = extract_data(
        fpath,
        subsystem_type="tr3",
        subsystem_info_mapper={
            "winding_1_bus_number": "WIND1NUMBER",
            "winding_2_bus_number": "WIND2NUMBER",
            "winding_3_bus_number": "WIND3NUMBER",
            "branch_id": "ID",
            "xfr_name": "XFRNAME",
            "pos_seq_impedance_1_2_pu": "RX1-2NOM",
            "pos_seq_impedance_2_3_pu": "RX2-3NOM",
            "pos_seq_impedance_3_1_pu": "RX3-1NOM",
            "zero_seq_impedance_1_pu": "Z01",
            "zero_seq_impedance_2_pu": "Z02",
            "zero_seq_impedance_3_pu": "Z03",
            "vector_group": "VECTORGROUP",
        },
    )

    return info_dict


def extract_winding_definitions(fpath: str) -> List[Dict[str, Any]]:
    """Extract three winding transformer winding data"""

    # TODO: Incomplete, need more values
    info_dict = extract_data(
        fpath,
        subsystem_type="wnd",
        subsystem_info_mapper={
            "winding_bus_number": "WNDBUSNUMBER",
            "winding_number": "WNDNUMBER",
            "controlled_bus_number": "ICONTNUMBER",
        },
    )

    return info_dict


def extract_bus_values(fpath: str) -> List[Dict[str, Any]]:
    """Extract PSSE scenario bus values"""

    info_dict = extract_data(
        fpath,
        subsystem_type="bus",
        subsystem_info_mapper={
            "bus_number": "NUMBER",
            "bus_voltage_pu": "PU",
            "bus_voltage_kv": "KV",
            "bus_voltage_angle_deg": "ANGLED",
        },
    )
    return info_dict


def extract_branch_values(
    fpath: str,
) -> List[Dict[str, Any]]:
    """Extract PSSE scenario branch values"""

    info_dict = extract_data(
        fpath,
        subsystem_type="brn",
        subsystem_info_mapper={
            "from_bus_number": "FROMNUMBER",
            "to_bus_number": "TONUMBER",
            "branch_id": "ID",
            "active_power_mw": "P",
            "reactive_power_mvar": "Q",
        },
    )
    return info_dict


def extract_machine_values(
    fpath: str,
) -> List[Dict[str, Any]]:
    """Extract PSSE scenario machine values"""

    info_dict = extract_data(
        fpath,
        subsystem_type="mach",
        subsystem_info_mapper={
            "bus_number": "NUMBER",
            "machine_id": "ID",
            "mbase_mva": "MBASE",
            "active_power_mw": "PGEN",
            "reactive_power_mvar": "QGEN",
            "pmax": "PMAX",
            "pmin": "PMIN",
            "qmax": "QMAX",
            "qmin": "QMIN",
        },
    )
    return info_dict
