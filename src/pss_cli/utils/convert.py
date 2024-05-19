from typing import Dict, List, Tuple


def get_list_of_dict(keys: List[str], list_of_tuples: List[Tuple]) -> List[Dict]:
    """This function will accept keys and list_of_tuples as args and return list of dicts"""

    list_of_dict = [dict(zip(keys, values)) for values in list_of_tuples]
    return list_of_dict
