import re
import versup.template as template
from versup.conf_reader import get_conf_value
from colorama import Style


def update_file_data(data, replace_list):
    regex = replace_list[0]
    new_text = replace_list[1]

    updated_data = re.sub(regex, new_text, data, flags=re.M)
    return updated_data


def show_updates(filename, data, replace_list):
    regex = replace_list[0]
    new_text = replace_list[1]

    lines = data.split("\n")
    for line in lines:
        line = line.strip()
        m = re.match(regex, line)
        if m:
            updated_data = re.sub(regex, new_text, line, flags=re.M)
            print(
                "In file {3}{0}{4} replace {3}{1}{4} with {3}{2}{4}".format(
                    filename, line, updated_data, Style.BRIGHT, Style.RESET_ALL
                )
            )


def update_files(new_version, files, dryrun):
    if not files:
        # No files to update
        return

    filenames = list(files.keys())
    template_data = {"version": new_version}

    for filename in filenames:
        try:
            with open(filename, "r") as file_h:
                data = file_h.read()
        except FileNotFoundError:
            print("Unable to find {} to update.".format(filename))
            continue

        # If it's only one entry make it a list to simplify program flow
        if not any(isinstance(el, list) for el in files[filename]):
            files[filename] = [files[filename]]

        for replace in files[filename]:
            replace[1] = template.render(replace[1], template_data)
            if dryrun:
                show_updates(filename, data, replace)
            else:
                data = update_file_data(data, replace)

        if not dryrun:
            with open(filename, "w") as file_h:
                file_h.write(data)
