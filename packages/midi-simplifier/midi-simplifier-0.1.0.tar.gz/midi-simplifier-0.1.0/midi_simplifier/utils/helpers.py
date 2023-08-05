from typing import Any, Type


def isoneof(value: Any, lst: list[Type]) -> bool:
    for T in lst:
        if isinstance(value, T):
            return True
    return False


def areoneof(values: list[Any], lst: list[Type]) -> bool:
    for v in values:
        if not isoneof(v, lst):
            return False

    return True


def notempty(lst: list[Any], msg: str = None) -> bool:
    if len(lst) != 0:
        return True
    raise ValueError(msg | "list must not be empty")
