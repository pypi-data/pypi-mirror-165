from typing import Any, Type, Callable


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


def check_foreach(lst: list[Any], condition: Callable[[Any], bool]) -> bool:
    for v in lst:
        if not condition(v):
            return False
    return True
