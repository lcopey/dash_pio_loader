"""
Basic Appshell with header and  navbar that collapses on mobile.  Also includes a theme switch.
"""

import dash_mantine_components as dmc
from dash import (
    Dash,
    _dash_renderer,  # noqa
    Input,
    Output,
    State,
    callback,
    clientside_callback,
    no_update,
)
from dash.dcc import Graph
from .components import make_theme_switch, make_header, make_nav_bar, make_nav_tree
from .app_ids import IDS
import logging
from pathlib import Path
import plotly.io as pio

logging.basicConfig(level=logging.DEBUG)

_dash_renderer._set_react_version("18.2.0")  # noqa

app = Dash(external_stylesheets=dmc.styles.ALL)
theme_toggle = make_theme_switch(id=IDS.switch_theme)

layout = dmc.AppShell(
    [
        make_header(theme_toggle, "PIO Loader"),
        make_nav_bar(
            children=make_nav_tree(id=IDS.tree, path="./"),
            title="Root folder",
            id=IDS.navbar,
        ),
        dmc.AppShellMain(["Main", Graph(id=IDS.figure)]),
    ],
    header={"height": 60},
    padding="md",
    navbar={
        "width": 300,
        "breakpoint": "sm",
        "collapsed": {"mobile": True},
    },
    id=IDS.app_shell,
)

app.layout = dmc.MantineProvider(layout)


@callback(
    Output(IDS.app_shell, "navbar"),
    Input("burger", "opened"),
    State(IDS.app_shell, "navbar"),
)
def navbar_is_open(opened, navbar):
    navbar["collapsed"] = {"mobile": not opened}
    return navbar


clientside_callback(
    """ 
    (switchOn) => {
       document.documentElement.setAttribute('data-mantine-color-scheme', switchOn ? 'dark' : 'light');  
       return window.dash_clientside.no_update
    }
    """,
    Output(IDS.switch_theme, "id"),
    Input(IDS.switch_theme, "checked"),
)


@callback(Output(IDS.figure, "figure"), Input(IDS.tree, "selected"))
def on_selection(selected):
    if selected:
        selected = Path(selected[0])
        if selected.is_file():
            return pio.read_json(selected)
    return no_update


if __name__ == "__main__":
    app.run(debug=True)
