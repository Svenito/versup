import versup.conf_reader as conf_reader
import pytest
import os

try:
    from unittest.mock import patch, mock_open
except ImportError:
    from mock import patch, mock_open


@pytest.fixture()
def config_file():
    yield conf_reader.parse_config_file("./tests/test_conf.json")


def test_parse_config_file():
    conf = conf_reader.parse_config_file("./tests/test_conf.json")
    assert conf["scripts"]["postbump"] == "echo POST"
    conf = conf_reader.parse_config_file("./tests/testsss_conf.json")
    assert conf == {}


def test_merge():
    a = {
        "test": "value",
        "another test": {"More values": 1, "another": 2},
        "c": {"x": 9, "o": 10},
    }
    b = {
        "test": "bvalue",
        "B another test": {"More values": 1, "another": 2},
        "c": {"x": 9, "y": 10},
    }
    c = conf_reader.merge(a, b)
    assert c["test"] == "bvalue"
    assert c["another test"] == {"More values": 1, "another": 2}
    assert c["c"] == {"x": 9, "y": 10, "o": 10}


def test_get_conf_value(config_file):
    a = conf_reader.get_conf_value(config_file, "scripts/postbump")
    assert a == "echo POST"
    b = conf_reader.get_conf_value(config_file, "scripts/postbumpdddd")
    assert b is None


def test_write_default_to_home():
    open_mock = mock_open()
    with patch("os.path.isfile", lambda x: False, create=True):
        with patch("versup.conf_reader.open", open_mock, create=True):
            conf_reader.write_default_to_home()
    open_mock.assert_called_with(os.path.expanduser("~/.config/versup.json"), "w+")


def test_merge_configs_with_default(config_file):
    import json

    open_mock = mock_open(read_data=json.dumps(config_file))
    with patch("versup.conf_reader.write_default_to_home", return_value=""):
        try:
            with patch("builtins.open", open_mock, create=True):
                output = conf_reader.merge_configs_with_default()
        except ImportError:
            with patch("__builtin__.open", open_mock, create=True):
                output = conf_reader.merge_configs_with_default()
    assert output["scripts"]["prebump"] == "echo PRE"


def test_parse_config_file_empty_file():
    conf = conf_reader.parse_config_file("./tests/test_conf_empty.json")
    assert conf == {}


def test_parse_config_file_non_existing_file():
    conf = conf_reader.parse_config_file("./tests/no_such_file.json")
    assert conf == {}