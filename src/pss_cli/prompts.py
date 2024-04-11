import re
from typing import List
from pathlib import Path
from InquirerPy import inquirer

from pss_cli.database import select_table


def get_parameter_from_string(input_strings: List[str], parameter: str):
    matches = [
        re.search(f"{parameter}='([^']+)'|{parameter}=([\d.]+)", input_string)
        for input_string in input_strings
    ]

    parameters = [match.group(1) or match.group(2) for match in matches]

    return parameters


def prompt_case_path(root_dir: str, match_pattern: str):
    """Prompt the user to select a file path"""

    files = list(Path(root_dir).rglob(match_pattern))

    _root_dir = Path(root_dir).absolute()

    if not files:
        print(
            f"No files with match-pattern '{match_pattern}' found within '{_root_dir}' and subdirectories."
        )
        return

    # fpath = fzf.prompt(files)
    fpath = inquirer.select(
        message="Select a case file from disk.",
        long_instruction="Select a PSSE sav case from the above file paths, relative to the current directory.",
        choices=files,
        border=True,
    ).execute()

    return fpath


def prompt_table(table_name: str, parameter: str):
    """Return a checkbox selection of table rows from the database"""

    objects = select_table(table_name)

    results = inquirer.checkbox(
        message=f"Select objects from database table '{table_name}'",
        long_instruction="Press <a> to toggle all, <space> to select, <enter> to finish selection.",
        choices=objects,
        keybindings={"toggle-all": [{"key": "a"}]},
        transformer=lambda x: get_parameter_from_string(x, parameter),
        border=True,
    ).execute()

    if None in results:
        print("No results found.")
        return None

    return results
