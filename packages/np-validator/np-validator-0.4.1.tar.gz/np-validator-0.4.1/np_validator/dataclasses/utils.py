from types import ModuleType
from typing import Any, Callable, List

import inspect


def is_mod_function(mod: ModuleType, func: Callable[..., Any]) -> bool:
    """checks that func is a function defined in module mod"""
    return inspect.isfunction(func) and inspect.getmodule(func) == mod


def list_functions(mod: ModuleType) -> List[Callable[..., Any]]:
    """list of functions defined in module mod"""
    return [
        func.__name__ for func in mod.__dict__.values() if is_mod_function(mod, func)
    ]


def resolve_function(mod: ModuleType, function_name: str) -> Callable[..., Any]:
    """resolves a module instance and function name to a callable function"""
    try:
        func = getattr(mod, function_name)
    except KeyError:
        raise Exception(f"Couldn't resolve function: {function_name} from: {mod}")

    if not callable(func):
        raise Exception(f"Resolved a non-callable function: {func} from: {mod}")

    return func  # type: ignore
