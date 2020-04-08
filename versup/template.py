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


def merge_data(x, y):
    z = x.copy()  # start with x's keys and values
    z.update(y)  # modifies z with y's keys and values & returns None
    return z


def render(string, data={}):
    # Merge new data with default
    new_data = merge_data(token_data, data)
    for k, v in new_data.items():
        # Check if value is not None and if the key is valid
        if v and (k in token_data.keys()):
            string = re.sub(r"\[{}\]".format(k), v, string, flags=re.M)

    return string
