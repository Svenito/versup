from __future__ import print_function
import re
import versup.template as template
from colorama import Style


def update_file_data(data, replace_list):
    """
    The replace list is a list of two strings, the first is a regex
    defining what is to be replaced, the second the text to replace the
    matches with
    :data: the source data on which to run the replace on
    :replace_list: list of a regex string and the string to replace with

    :returns: the updated data
    """
    regex = replace_list[0]
    new_text = replace_list[1]

    updated_data = re.sub(regex, new_text, data, flags=re.M)
    return updated_data


def show_updates(filename, data, replace_list):
    """
    This is the same as :update_file_data: but for dry runs. It will
    search for the matches to replace and print out the changes that will
    occur instead of actually updating the files
    """
    regex = replace_list[0]
    new_text = replace_list[1]

    lines = data.split("\n")
    for line in lines:
        line = line.strip()
        m = re.search(regex, line)
        if m:
            updated_data = re.sub(regex, new_text, line, flags=re.M)
            print(
                u"In file {3}{0}{4} replace {3}{1}{4} with {3}{2}{4}".format(
                    filename, line, updated_data, Style.BRIGHT, Style.RESET_ALL
                )
            )


def update_files(new_version, files, dryrun):
    """
    Will update the given files with the defined regex from
    the config files and the text to replace with

    :new_version: the new version for the next release
    :files: a list of filenames with path on which to run the replace
    :dryrun: boolean flag whether to do a dry run or not
    """
    if not files:
        # No files to update
        return []

    filenames = list(files.keys())
    template_data = {"version": new_version}
    updated_files = []
    for filename in filenames:
        try:
            with open(filename, "r") as file_h:
                data = file_h.read()
        except IOError:
            print("Unable to find {} to update.".format(filename))
            continue

        updated_files.append(filename)

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

    return updated_files
