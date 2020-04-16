import versup.file_updater as file_updater
import pytest
import os
from unittest.mock import patch, mock_open
import sys
import io


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
    files = {temp_file.realpath(): ["1.2.3", "3.4.5"]}
    file_updater.update_files("3.4.5", files, False)
    assert temp_file.read() == "this is a file to replace 3.4.5 with new version"


def test_dry_run(tmpdir):
    temp_file = tmpdir.join("testfile.txt")
    temp_file.write("this is a file to replace 1.2.3 with new version")
    files = {temp_file.realpath(): ["1.2.3", "3.4.5"]}

    capturedOutput = io.StringIO()
    sys.stdout = capturedOutput

    file_updater.update_files("3.4.5", files, True)

    sys.stdout = sys.__stdout__
    output = capturedOutput.getvalue().split("\n")

    assert "with" in output[0]
    assert "replace 3.4.5" in output[0]
