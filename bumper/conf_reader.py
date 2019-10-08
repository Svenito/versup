import os
import json
from bumper.default_conf import default_conf


def parse_config_file():
    cwd = os.getcwd()
    with open(os.path.join(cwd, "bumper.json"), "r") as conf_file:
        d = json.loads(conf_file.read())
    return d


def merge_config_with_default():
    # TODO: Add support for user, local, and dynamic settings
    try:
        config = parse_config_file()
    except:
        return default_conf

    for k in config.keys():
        default_conf[k] = config[k]
    return default_conf


def get_conf_value(key_path):
    paths = key_path.split("/")
    root = default_conf

    for p in paths:
        try:
            v = root[p]
            root = v
        except KeyError:
            break
    return v