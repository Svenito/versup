import re
import bumper.template as template
from bumper.conf_reader import get_conf_value


def update_file_data(data, replace_list):
    regex = replace_list[0]
    new_text = replace_list[1]

    updated_data = re.sub(regex, new_text, data, flags=re.M)
    return updated_data


def update_files(new_version, files):
    if files is None:
        # No files to update
        return

    filenames = list(files.keys())

    for filename in filenames:
        try:
            with open(filename, "r") as file_h:
                data = file_h.read()
        except FileNotFoundError:
            print("Unable to find {} to update.".format(filename))
            continue

        # If it's only one entry make it a list to simply program flow
        if not any(isinstance(el, list) for el in files[filename]):
            files[filename] = [files[filename]]

        template.token_data["version"] = new_version
        for replace in files[filename]:
            replace[1] = template.render(replace[1])
            data = update_file_data(data, replace)

        with open(filename, "w") as file_h:
            file_h.write(data)
