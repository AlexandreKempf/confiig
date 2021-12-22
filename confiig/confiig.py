import importlib
import inspect
import os
import sys
from functools import partial
from typing import Any, Tuple


def add_context(f, *args, **kwargs):
    """[summary]

    Args:
        f ([type]): [description]

    Raises:
        Exception: [description]

    Returns:
        [type]: [description]
    """
    if callable(f):
        argument_names = inspect.getfullargspec(f)[0]
        if len(args) + len(kwargs) >= len(argument_names):
            return f(
                *args[: len(argument_names)],
                **{k: v for k, v in kwargs.items() if k in argument_names},
            )
        else:
            f_name = getattr(f, "__name__", repr(f))
            raise Exception(
                f"the function '{f_name}' expect at maximum {len(args)+len(kwargs)} arguments"
            )
    else:
        return f


def find_smallest_module(dir_path: str, file_path: str) -> Tuple[str, str]:
    if os.path.exists(os.path.join(dir_path, "__init__.py")):
        return dir_path, file_path
    else:
        dir_path, last_dir = os.path.split(dir_path)
        file_path = os.path.join(last_dir, file_path)
        return find_smallest_module(dir_path, file_path)


def import_config(file_path: str) -> object:
    dir_name, file_name = os.path.split(os.path.abspath(file_path))
    module, submodule = find_smallest_module(dir_name, file_name)
    submodule = os.path.splitext(submodule)[0]
    if module not in sys.path:
        sys.path.insert(0, module)
    return importlib.import_module(submodule.replace("/", "."))


# a = import_config("hyperbolic_time_chamber/training/tweaks/league-of-legends/stats/champions/train.py")

# #context
# foo = "one "
# index = "two "
# array = "three"


# # configuration
# def map(foo):
#     return foo

# print(add_context(map, foo, index, array))

# def map(foo, index):
#     return foo + index

# print(add_context(map, foo, index, array))

# map = partial(map, index="deux")

# print(add_context(map, foo, index, array))

# def map(foo, index, array):
#     return foo + index + array

# print(add_context(map, foo, index, array))
