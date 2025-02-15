"""
>>> class AppIds(BaseIds):
...     value = auto()
>>> AppIds()
AppIds(value='value')

>>> class InnerValue(BaseIds):
...     value = auto()
>>> class AppIds(BaseIds):
...     value = InnerValue()
>>> AppIds()
AppIds(value=InnerValue(value='value'))

"""

from abc import ABCMeta


class auto:
    pass


def _is_dunder_or_private(key: str):
    return (key.startswith("__") and key.endswith("__")) or (key.startswith("_"))


class IdsMeta(ABCMeta):
    def __new__(cls, name: str, bases, dct):
        for key, value in dct.items():
            if not _is_dunder_or_private(key):
                if isinstance(value, auto):
                    dct[key] = key

        instance = super().__new__(cls, name, bases, dct)
        return instance


class BaseIds(metaclass=IdsMeta):
    def __repr__(self):
        attrs = [value for value in dir(self) if not _is_dunder_or_private(value)]
        text = [f"{attr}={getattr(self, attr)!r}" for attr in attrs]
        text = ", ".join(text)
        return f"{self.__class__.__name__}({text})"
