import re


def do_replace(data, replace_list, new_version):
    regex = replace_list[0]
    new_text = replace_list[1]

    new_text = re.sub(r"\[version\]", new_version, new_text)
    updated_data = re.sub(regex, new_text, data, flags=re.M)
    return updated_data


def update_files(conf, new_version):
    try:
        file_re = conf["files"]
    except KeyError:
        # No files to update
        return

    filenames = list(file_re.keys())

    for filename in filenames:
        try:
            with open(filename, "r") as file_h:
                data = file_h.read()
        except FileNotFoundError:
            print("Unable to find {} to update.".format(filename))
            continue

        # If it"s only one entry make it a list to simply program flow
        if not any(isinstance(el, list) for el in file_re[filename]):
            file_re[filename] = [file_re[filename]]

        for replace in file_re[filename]:
            data = do_replace(data, replace, new_version)

        with open(filename, "w") as file_h:
            file_h.write(data)

