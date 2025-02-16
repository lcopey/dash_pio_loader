from typing import Callable

import dash_mantine_components as dmc
from dash_iconify import DashIconify
from pathlib import Path
import logging
from functools import cmp_to_key

logging.basicConfig(level=logging.DEBUG)


def make_theme_switch(id: str):
    return dmc.Switch(
        offLabel=DashIconify(
            icon="radix-icons:sun",
            width=15,
            color=dmc.DEFAULT_THEME["colors"]["yellow"][8],
        ),
        onLabel=DashIconify(
            icon="radix-icons:moon",
            width=15,
            color=dmc.DEFAULT_THEME["colors"]["yellow"][6],
        ),
        id=id,
        persistence=True,
        color="grey",
    )


def make_header(children, title: str):
    return dmc.AppShellHeader(
        dmc.Group(
            [
                dmc.Group(
                    [
                        dmc.Burger(
                            id="burger",
                            size="sm",
                            hiddenFrom="sm",
                            opened=False,
                        ),
                        dmc.Title(title, c="blue"),
                    ]
                ),
                children,
            ],
            justify="space-between",
            style={"flex": 1},
            h="100%",
            px="md",
        ),
    )


def make_nav_bar(children, title: str, id: str):
    return dmc.AppShellNavbar(
        id=id,
        children=[title, children],
        p="md",
    )


def walk_directory(path: Path, predicate: Callable[[Path], bool]):
    children = list()
    current_node = {"value": str(path), "label": path.name}
    for child in path.iterdir():
        if child.is_dir():
            nested_node = walk_directory(child, predicate)
            if nested_node:
                children.append(nested_node)
        elif child.is_file() and predicate(child):
            children.append({"value": str(child), "label": child.name})
    if children:
        current_node["children"] = children
    return current_node


def sort_nodes(nodes: list):
    def comparison(a, b) -> int:
        a = Path(a["value"])
        b = Path(b["value"])
        if a.is_dir() and b.is_dir():
            return 0 if str(a) > str(b) else -1
        elif a.is_file() and b.is_dir():
            return 0
        elif a.is_dir() and b.is_file():
            return -1
        else:
            return 0 if a.name > b.name else -1

    nodes = sorted(nodes, key=cmp_to_key(comparison))
    for node in nodes:
        if "children" in node:
            node["children"] = sort_nodes(node["children"])
    return nodes


def filter_nodes(nodes: list):
    filtered = []
    for node in nodes:
        value = Path(node["value"])
        if not (value.is_dir() and "children" not in node):
            filtered.append(node)
        if "children" in node:
            node["children"] = filter_nodes(node["children"])
    return filtered


def make_nav_tree(path: Path | str, id: str):
    if not isinstance(path, Path):
        path = Path(path)

    nodes = walk_directory(path, predicate=lambda x: x.name.endswith(".jpg"))
    nodes = [nodes]
    nodes = filter_nodes(nodes)
    nodes = sort_nodes(nodes)

    return dmc.Tree(id=id, data=nodes)
