import dash_mantine_components as dmc
from dash_iconify import DashIconify


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

def make_nav_bar(children, title):
    return dmc.AppShellNavbar(
        id="navbar",
        children=[
            title,
            children
        ],
        p="md",
    )
