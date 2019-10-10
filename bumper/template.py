import re


token_data = {
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


def render(string):
    for k, v in token_data.items():
        if v:
            string = re.sub(r"\[${}\]".format(k), v, string, flags=re.M)

    return string
