import pytest

import versup.changelog as changelog

try:
    from unittest.mock import Mock, patch
except ImportError:
    from mock import patch, Mock

import io
import sys


def mocked_get_commit_messages():
    return [
        {
            "hash": "0820a11b306a78c184b183ac0820a11b30f80500",
            "author_name": "Author",
            "author_email": "user@mail.com",
            "date": "1586565955",
            "message": "Message 1",
        },
        {
            "hash": "72da59cde34278c184b183ac0820a11b30f80511",
            "author_name": "Author",
            "author_email": "user@mail.com",
            "date": "1586965934",
            "message": "Message 2",
        },
        {
            "hash": "beefca2e856978c184b183ac0820a11b30f80522",
            "author_name": "Author",
            "author_email": "user@mail.com",
            "date": "1586955955",
            "message": "Message 3",
        },
    ]


@pytest.fixture(scope="session")
def filename(tmpdir_factory):
    filename = tmpdir_factory.mktemp("versup").join("changelog.txt")
    with open(str(filename), "w") as f:
        f.write("this is a line\n")
        f.write("This is another line\n")
    return filename


def test_write_new_changelog(tmpdir):
    filename = tmpdir.join("new_changelog.txt")
    with patch("versup.gitops.get_commit_messages", mocked_get_commit_messages):
        changelog.write(
            str(filename),
            "Version [version]",
            "- [message]",
            "\n",
            False,
            "1.2.3",
            False,
        )
    with open(str(filename)) as f:
        newlog = f.read()
    assert newlog.split("\n")[0] == "Version 1.2.3"
    assert newlog.split("\n")[1] == "- Message 1"
    assert newlog.split("\n")[2] == "- Message 2"
    assert newlog.split("\n")[3] == "- Message 3"
    assert len(newlog.split("\n")) == 6


def test_update_changelog(filename):
    with patch("versup.gitops.get_commit_messages", mocked_get_commit_messages):
        changelog.write(
            str(filename),
            "Version [version]",
            "- [message]",
            "\n",
            False,
            "1.2.3",
            False,
        )
    with open(str(filename)) as f:
        newlog = f.read()

    assert newlog.split("\n")[0] == "Version 1.2.3"
    assert newlog.split("\n")[1] == "- Message 1"
    assert newlog.split("\n")[2] == "- Message 2"
    assert newlog.split("\n")[3] == "- Message 3"
    assert newlog.split("\n")[5] == "this is a line"
    assert newlog.split("\n")[6] == "This is another line"
    assert len(newlog.split("\n")) == 8


@patch("os.system")
def test_show_file_linux_custom_editor(os_system):
    import os

    os.environ["EDITOR"] = "/usr/bin/editor"
    changelog.show_file("/tmp/file")
    os_system.assert_called_once_with("/usr/bin/editor /tmp/file")


@patch("os.system")
def test_show_file_linux_vi(os_system):
    import os

    os.environ.pop("EDITOR", None)
    changelog.show_file("/tmp/file")
    os_system.assert_called_once_with("vi /tmp/file")


@patch("os.system")
def test_show_file_windows(os_system):
    with patch("sys.platform", Mock(return_value="win32")):
        sys.platform = "win32"
        changelog.show_file("/tmp/file")
    os_system.assert_called_once_with("notepad.exe /tmp/file")


def test_dryrun(filename):
    capturedOutput = io.StringIO()
    sys.stdout = capturedOutput

    with patch("versup.gitops.get_commit_messages", mocked_get_commit_messages):
        changelog.write(
            filename,
            "Version [version]",
            "- [message]",
            "\n",
            False,
            "1.2.3",
            True,
        )
    sys.stdout = sys.__stdout__
    output = capturedOutput.getvalue().split("\n")
    assert output[0] == "Writing changelog entries:"
    assert output[1] == ""
    assert output[2] == "- Message 1"
