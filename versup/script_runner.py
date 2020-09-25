import subprocess

from versup.conf_reader import get_conf_value


def prepost_script(taskname):
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

    def doit(function):
        def wrapper(config, version, **kwargs):
            pre_script = get_conf_value(config, "scripts/pre{}".format(taskname))

            if pre_script:
                if kwargs["dryrun"]:
                    print("Execute pre script `{}`\n".format(pre_script))
                else:
                    subprocess.call(pre_script.split() + [version])

            value = function(config, version, **kwargs)

            post_script = get_conf_value(config, "scripts/post{}".format(taskname))
            if post_script:
                if kwargs["dryrun"]:
                    print("Execute post script `{}`\n".format(post_script))
                else:
                    subprocess.call(post_script.split())

            return value

        return wrapper

    return doit
