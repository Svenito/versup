import subprocess

from bumper.conf_reader import get_conf_value


def bump(func):
    def inner(conf, version):
        pre_script = get_conf_value(conf, "scripts/prebump")
        if pre_script:
            subprocess.run(pre_script.split() + [version])

        value = func(conf, version)

        post_script = get_conf_value(conf, "scripts/postbump")
        if post_script:
            subprocess.run(post_script.split())

        return value

    return inner
