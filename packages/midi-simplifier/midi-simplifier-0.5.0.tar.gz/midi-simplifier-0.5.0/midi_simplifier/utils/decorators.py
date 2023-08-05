from typing import Callable, Type, Any, Union, Tuple
import functools
from .helpers import isoneof


def memo(func):
    cache = {}

    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrapper


def validate(*args) -> Callable:
    """validate decorator

        Is passed types of variables to preforme type checking over
        The arguments must be passed in the same order

        for each parameter respectivly you can choose three things:
        1. None - to skip
        2. Type - a type to check 
        3. Tuple/list - (Union[Type, list[Type]], Callable[[Any], bool], str)
            where Type is the type for type checking validation,
            condition is a function to call on the value which return bool.
            msg is the msg to raise inside the ValueError when ondition fails

    Returns:
        Callable: return decorated function
    """
    def wrapper(func: Callable) -> Callable:
        n_arg = func.__code__.co_argcount
        l_arg: list[str] = func.__code__.co_varnames[:n_arg]
        for i, var_name in enumerate(l_arg):
            if var_name not in func.__annotations__:
                func.__annotations__[var_name] = args[i]

        def validate_type(v: Any, T: Type, validation_func: Callable[[Any], bool] = isinstance) -> None:
            if not validation_func(v, T):
                raise TypeError(
                    f"In {func.__module__}.{func.__name__}(...) argument number {i+1}: is '{ v }' and is of type '{type(v)}' but must be of type '{T}'")

        def validate_condition(v: Any, condition: Callable[[Any], bool], msg: str = None) -> None:
            if not condition(v):
                raise ValueError(
                    msg or f"In {func.__module__}.{func.__name__}(...), argument: '{str(v)}' doesnt comply with constraints given in {condition.__module__}.{condition.__name__}")

        @functools.wraps(func)
        def inner(*innerargs, **innerkwargs) -> Any:
            for i in range(min(len(args), len(innerargs))):
                if args[i] is not None:
                    if isoneof(args[i], [list, Tuple]):
                        class_type, condition = args[i][0], args[i][1]

                        # Type validation
                        if isoneof(class_type, [list, Tuple]):
                            validate_type(innerargs[i], class_type, isoneof)
                        else:
                            validate_type(innerargs[i], class_type, isinstance)

                        # constraints validation
                        if condition is not None:
                            message = args[i][2] if len(args[i]) > 2 else None
                            validate_condition(
                                innerargs[i], condition, message)
                    else:
                        validate_type(innerargs[i], args[i])
            return func(*innerargs, **innerkwargs)
        return inner
    return wrapper


@ validate(str, Type, bool, Callable, str)
def opt(opt_name: str, opt_type: Type, is_required: bool = True, constraints: Callable[[Any], bool] = None, constraints_description: str = None) -> Callable:
    """the opt decorator is to easily handle function options

    Args:
        name (str): name of option
        type (Type): type of option
        required (bool, optional): if this option is required. Defaults to True.
        constraints (Callable[[Any], bool], optional): a function to check constraints on the option. Defaults to None.
        constraints_description (str, optional): a message to show if constraints check fails. Defaults to None.

    Returns:
        Callable: return decorated function
    """
    def wrapper(func):
        @ functools.wraps(func)
        def inner(*args, **kwargs):
            if is_required and args[0] is None:
                raise ValueError(
                    f"{opt_name} was marked as required and got None")
            if not isinstance(args[0], opt_type):
                raise TypeError(
                    f"{opt_name} has value of wrong type: {args[0]} which is {type(args[0])} instead of {opt_type}")
            return func(*args, **kwargs)
        return inner
    return wrapper
