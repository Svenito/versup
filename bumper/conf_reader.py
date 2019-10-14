import os
import json
from bumper.default_conf import default_conf


config_files = ["./bumper.json", "~/.bumper.json"]


def parse_config_file(config_file):
    cwd = os.getcwd()
    d = {}
    try:
        with open(os.path.expanduser(config_file), "r") as conf_file:
            d = json.loads(conf_file.read())
    except FileNotFoundError:
        pass
    return d


def merge(a, b, path=None):
    "merges b into a"
    if path is None: path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass # same leaf value
            else:
                a[key] = b[key]
        else:
            a[key] = b[key]
    return a


def merge_configs_with_default():
    # TODO: Add support for user, local, and dynamic settings
    current_config = default_conf
    for config_file in config_files:
        config = parse_config_file(config_file)
        merge(current_config, config)
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
