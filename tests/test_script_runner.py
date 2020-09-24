import versup.script_runner as script_runner
import versup.conf_reader as conf_reader

import pytest

try:
    from unittest.mock import patch, call
except ImportError:
    from mock import patch, call


@pytest.fixture()
def config_file():
    yield conf_reader.parse_config_file("./tests/test_conf.json")


@patch("subprocess.call")
def test_script_runner(subprocess_run, config_file):
    @script_runner.prepost_script("bump")
    def func(c_file, version, **kwargs):
        pass

    func(config_file, "1.0.2", dryrun=True)
    subprocess_run.assert_not_called()

    func(config_file, "1.0.2", dryrun=False)
    call1 = call(["echo", "PRE", "1.0.2"])
    call2 = call(["echo", "POST"])
    subprocess_run.assert_has_calls([call1, call2])
