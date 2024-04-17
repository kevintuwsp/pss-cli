from typing import Optional
from pathlib import Path
from InquirerPy import inquirer
from sqlmodel import SQLModel
from functools import partial

from pss_cli.utils.regex import get_parameter_from_string, get_parameter_from_strings
from pss_cli.core.database import db


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
    fpath = inquirer.fuzzy(
        message="Select a case file from disk.",
        long_instruction="Select a PSSE sav case from the above file paths, relative to the current directory.",
        choices=files,
        border=True,
    ).execute()

    return fpath


def prompt_select_table(table_name: str, parameter: Optional[str]) -> SQLModel:
    """Return a checkbox selection of table rows from the database"""

    objects = db.select_table(table_name)

    transformer = None
    if parameter:
        transformer = partial(get_parameter_from_string, parameter=parameter)

    results = inquirer.select(
        message=f"Select objects from database table '{table_name}'",
        long_instruction="Press <space> to select, <enter> to finish selection.",
        choices=objects,
        transformer=transformer,
        border=True,
    ).execute()

    if None in results:
        print("No results found.")
        return None

    return results


def prompt_table(table_name: str, parameter: str) -> SQLModel:
    """Return a checkbox selection of table rows from the database"""

    objects = db.select_table(table_name)

    results = inquirer.checkbox(
        message=f"Select objects from database table '{table_name}'",
        long_instruction="Press <a> to toggle all, <space> to select, <enter> to finish selection.",
        choices=objects,
        keybindings={"toggle-all": [{"key": "a"}]},
        transformer=lambda x: get_parameter_from_strings(x, parameter),
        border=True,
    ).execute()

    if None in results:
        print("No results found.")
        return None

    return results


def prompt_table_names() -> str:
    """Return a selection of table names"""

    table_names = db.get_all_table_names()

    table_name = inquirer.fuzzy(
        message="Select a table from the database.",
        choices=table_names,
        border=True,
    ).execute()

    return table_name
