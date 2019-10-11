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
    current_config = default_conf
    try:
        config = parse_config_file()
    except:
        return current_config

    for k in config.keys():
        current_config[k] = config[k]
    return current_config


def get_conf_value(config_data, key_path):
    paths = key_path.split("/")
    root = config_data

    for p in paths:
        try:
            v = root[p]
            root = v
        except KeyError:
            return None
    return v
