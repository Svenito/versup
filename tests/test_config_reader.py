import versup.conf_reader as conf_reader
import pytest


@pytest.fixture()
def config_file():
    yield conf_reader.parse_config_file("./tests/test_conf.json")


class TestConfigReader:
    def test_parse_config_file(self):
        conf = conf_reader.parse_config_file("./tests/test_conf.json")
        assert conf["scripts"]["postbump"] == "echo POST"
        conf = conf_reader.parse_config_file("./tests/testsss_conf.json")

    def test_merge(self):
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

    def test_get_conf_value(self, config_file):
        a = conf_reader.get_conf_value(config_file, "scripts/postbump")
        assert a == "echo POST"
        b = conf_reader.get_conf_value(config_file, "scripts/postbumpdddd")
        assert b == None
