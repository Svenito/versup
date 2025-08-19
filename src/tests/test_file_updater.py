import versup.file_updater as file_updater
import pathlib


def test_update_file_data():
    x = file_updater.update_file_data(
        "this is the source string we need to hcange", [r"hcange", "change"]
    )
    assert x == "this is the source string we need to change"

    x = file_updater.update_file_data(
        "this is the source string we need to hcange", [r" s", " S"]
    )
    assert x == "this is the Source String we need to hcange"


def test_update_files():
    testfile = "testfile.txt"
    with open(testfile, "w") as temp_file:
        temp_file.write("this is a file to replace 1.2.3 with new version")
    files = {testfile: ["1.2.3", "3.4.5"]}
    print(files)
    file_updater.update_files("3.4.5", files, False)
    with open(testfile, "r") as temp_file:
        assert (
            temp_file.readline() == "this is a file to replace 3.4.5 with new version"
        )
    pathlib.Path.unlink(testfile)


def test_do_not_update_external_files(capfd):
    testfile = "/tmp/testfile.txt"
    with open(testfile, "w") as temp_file:
        temp_file.write("this is a file to replace 1.2.3 with new version")
    files = {testfile: ["1.2.3", "3.4.5"]}
    file_updater.update_files("3.4.5", files, False)
    out, err = capfd.readouterr()
    assert out == "Invalid file path /tmp/testfile.txt\n"
    with open(testfile, "r") as temp_file:
        assert (
            temp_file.readline() == "this is a file to replace 1.2.3 with new version"
        )

    pathlib.Path.unlink(testfile)


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
    testfile = "testfile.txt"
    with open(testfile, "w") as temp_file:
        temp_file.write("this is a file to replace 1.2.3 with new version")
    files = {testfile: ["1.2.3", "3.4.5"]}

    updated_files, updates = file_updater.update_files("3.4.5", files, True)

    assert testfile in updates.keys()
    assert "replace 3.4.5" in updates[testfile]
    pathlib.Path.unlink(testfile)
