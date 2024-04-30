import pathlib

from rich import print
from rich.tree import Tree


def print_ok(message: str):
    print(f"[green]:heavy_check_mark:[/green] {message}\n")


def print_error(message: str):
    print(f":boom: {message}\n")


def print_warn(message: str):
    print(f"[yellow]:double_exclamation_mark:[/yellow] {message}\n")


def add_to_tree(paths, tree, file_msg):
    if not paths:
        return tree

    p = paths.pop(0)
    t = tree.add(f"{p} : {file_msg.get(p, '') if file_msg else ''}")
    add_to_tree(paths, t, file_msg)


def make_file_tree(file_paths, file_msg=None):
    tree = Tree(":open_file_folder:")
    for file_path in file_paths:
        add_to_tree(list(pathlib.Path(file_path).parts), tree, file_msg)
    return tree
