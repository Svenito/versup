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


def merge_dicts(x, y):
    z = x.copy()  # start with x's keys and values
    z.update(y)  # modifies z with y's keys and values & returns None
    return z


def render(string, data={}):
    # Merge new data with default
    # use this when dropping python 2 support
    # new_data = {**token_data, **data}
    new_data = merge_dicts(token_data, data)

    for k, v in new_data.items():
        # Check if value is not None and if the key is valid
        if v and (k in token_data.keys()):
            string = re.sub(r"\[{}\]".format(k), v, string, flags=re.M)

    return string
