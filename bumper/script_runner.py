import subprocess

from bumper.conf_reader import get_conf_value


def prepost_script(taskname):
    def doit(function):
        def wrapper(config, version, **kwargs):
            pre_script = get_conf_value(config, "scripts/pre{}".format(taskname))

            if pre_script:
                if kwargs["dryrun"]:
                    print("Execute pre script `{}`".format(pre_script))
                else:
                    subprocess.run(pre_script.split() + [version])

            value = function(config, version, **kwargs)

            post_script = get_conf_value(config, "scripts/post{}".format(taskname))
            if post_script:
                if kwargs["dryrun"]:
                    print("Execute post script `{}`".format(post_script))
                else:
                    subprocess.run(post_script.split())

            return value

        return wrapper

    return doit
