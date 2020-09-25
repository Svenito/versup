import os
import json
from versup.default_conf import default_conf


config_files = [
    "~/.config/versup.json",
    "./.versup.json",
]


def write_default_to_home():
    """
    Copy the default settings to the user's home directory if
    it does not exist yet
    """
    home_file = os.path.expanduser(config_files[0])
    if not os.path.isfile(home_file):
        with open(home_file, "w+") as f:
            f.write(json.dumps(default_conf, indent=4))


def parse_config_file(config_file):
    d = {}
    try:
        with open(os.path.expanduser(config_file), "r") as conf_file:
            data = conf_file.read()
            if data:
                d = json.loads(data)
    except IOError:
        pass
    return d


def merge(a, b, path=None):
    """
    Recursively merges two dictionaries b into a. Duplicate keys, b overrides a
    """
    if path is None:
        path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass  # same leaf value
            else:
                a[key] = b[key]
        else:
            a[key] = b[key]
    return a


def merge_configs_with_default():
    current_config = {}
    for config_file in config_files:
        config = parse_config_file(config_file)
        merge(current_config, config)
    # Finally merge the default local and the current_config. This allows
    # adding new keys to the default config in future releases without
    # having to overwrite the user's home dir config
    current_config = merge(default_conf, current_config)
    return current_config


def get_conf_value(config_data, key_path):
    paths = key_path.split("/")
    root = config_data

    for p in paths:
        try:
            v = root[p]
            root = v
        except KeyError:
            # TODO: Raise here?
            return None
    return v
