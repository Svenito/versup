import subprocess
from typing import Any, Callable, Dict

from versup.conf_reader import get_conf_value


def prepost_script(taskname: str):
    """
    This a decorator function that will run the configured pre and post scripts
    defined in the config before and after calling one the decorated function.
    The decorator requires the name of the task, which will be used to match
    the script name in the config file

    eg. pretag, posttag would require a decorator like @prepost_script("tag")

    The original function must have an argument list like

    .. code:: python

        function(config, version, **kwargs)

    in order for the decorator to function correctly
    """

    def doit(function: Callable[..., Any]) -> Callable[..., Any]:
        def wrapper(config: Dict, version: str, **kwargs) -> Any:
            pre_script = get_conf_value(config, f"scripts/pre{taskname}")
            if pre_script:
                if kwargs["dryrun"]:
                    print(f"Execute pre script '{pre_script}'\n")
                else:
                    subprocess.call(pre_script.split() + [version])

            value = function(config, version, **kwargs)

            post_script = get_conf_value(config, f"scripts/post{taskname}")
            if post_script:
                if kwargs["dryrun"]:
                    print(f"Execute post script '{post_script}'\n")
                else:
                    subprocess.call(post_script.split())

            return value

        return wrapper

    return doit
