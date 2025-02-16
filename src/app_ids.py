from .ids import BaseIds, auto


class AppIds(BaseIds):
    app_shell = auto()
    switch_theme = auto()
    navbar = auto()
    tree = auto()


IDS = AppIds()
