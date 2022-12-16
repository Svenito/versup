import re
from typing import Dict, Union

token_data: Dict[str, Union[str, None]] = {
    "version": None,
    "version_date": None,
    "message": None,
    "date": None,
    "hash": None,
    "hash4": None,
    "hash7": None,
    "hash8": None,
    "author_name": None,
    "author_email": None,
}


def render(string: str, data: Dict[str, str] = {}):
    # Merge new data with default
    new_data: Dict[str, Union[str, None]] = {**token_data, **data}

    for k, v in new_data.items():
        # Check if value is not None and if the key is valid
        if v and (k in token_data.keys()):
            string = re.sub(rf"\[{k}\]", v, string, flags=re.M)

    return string
