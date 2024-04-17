import re

from typing import List


def get_parameter_from_strings(input_strings: List[str], parameter: str):
    matches = [
        re.search(f"{parameter}='([^']+)'|{parameter}=([\d.]+)", input_string)
        for input_string in input_strings
    ]

    parameters = [match.group(1) or match.group(2) for match in matches]

    return parameters


def get_parameter_from_string(input_string: str, parameter: str):
    match = re.search(f"{parameter}='([^']+)'|{parameter}=([\d.]+)", input_string)
    parameter = match.group(1) or match.group(2)

    return parameter
