import re

from typing import List

from sqlmodel import SQLModel


def get_parameter_from_strings(input_strings: List[str], parameter: str):
    matches = [
        re.search(f"{parameter}='([^']+)'|{parameter}=([\d.]+)", input_string)
        for input_string in input_strings
    ]

    parameters = [match.group(1) or match.group(2) for match in matches]

    return parameters


def get_parameter_from_string(input_string: str, parameter: str):
    print(input_string, type(input_string))
    match = re.search(f"{parameter}='([^']+)'|{parameter}=([\d.]+)", input_string)
    parameter = match.group(1) or match.group(2)

    return parameter


# def get_parameters_from_string(input_string: str, parameters: List[str]) -> List[str]:
def get_parameters_from_obj(obj: SQLModel, parameters: List[str]) -> str:
    parameter_str = " | ".join(
        [f"{parameter}={getattr(obj, parameter)}" for parameter in parameters]
    )
    return parameter_str
