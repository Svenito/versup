import versup.file_updater as file_updater


def test_update_file_data():
    x = file_updater.update_file_data(
        "this is the source string we need to hcange", [r"hcange", "change"]
    )
    assert x == "this is the source string we need to change"

    x = file_updater.update_file_data(
        "this is the source string we need to hcange", [r" s", " S"]
    )
    assert x == "this is the Source String we need to hcange"


def test_update_files(tmpdir):
    temp_file = tmpdir.join("testfile.txt")
    temp_file.write("this is a file to replace 1.2.3 with new version")
    files = {str(temp_file.realpath()): ["1.2.3", "3.4.5"]}
    print(files)
    file_updater.update_files("3.4.5", files, False)
    assert temp_file.read() == "this is a file to replace 3.4.5 with new version"


def test_return_empty_list_for_no_files():
    assert file_updater.update_files("3.4.5", {}, False) == ([], {})


def test_return_empty_list_if_file_not_found():
    assert file_updater.update_files(
        "3.4.5",
        {
            "doesnotexist": [
                ["Version ([\\d\\.]+) ", "Version [version] "],
                ["Version is ([\\d\\.]+)", "Version is [version]"],
            ]
        },
        False,
    ) == ([], {})


def test_dry_run(tmpdir):
    filename = "testfile.txt"
    temp_file = tmpdir.join(filename)
    temp_file.write("this is a file to replace 1.2.3 with new version")
    files = {str(temp_file.realpath()): ["1.2.3", "3.4.5"]}

    updated_files, updates = file_updater.update_files("3.4.5", files, True)

    assert filename in updates.keys()
    assert "replace 3.4.5" in updates[filename]
