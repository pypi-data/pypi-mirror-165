"""Hashing tools.
With data science tools in mind, the hashing should be possible
to perform on various data structures such as pandas.DataFrame,
nympy.array. The trade-off for simplicity is adding the libraries as
the project dependencies.
"""

import hashlib
import json
import typing as t
import inspect

import pandas as pd
import numpy as np


def _compute_hash(argument: t.Hashable) -> str:
    """Compute hash from the Python object argument."""
    argument = _make_hashable(argument)
    return str(hashlib.md5(json.dumps(argument).encode()).hexdigest())


def _make_hashable(arg: t.Any) -> t.Hashable:
    """Convert input argument to hashable type."""
    try:
        if isinstance(arg, pd.DataFrame):
            # pylint: disable=fixme
            # todo: check if it's faster to convert ot string or tuple
            return str(pd.util.hash_pandas_object(arg).values)
        if isinstance(arg, np.ndarray):
            return arg.tostring()  # type: ignore
        if callable(arg):
            return inspect.getsource(arg)
    except TypeError as exc:

        raise TypeError(
            f"Can't make the argument of a type {type(arg)} hashable. Only"
            "supported types are standard library types and "
            "pd.DataFrame, np.array."
        ) from exc

    return arg


def hash_arguments(args) -> t.List[str]:
    """Compute hash for all the arguments passed to the module."""
    return [_compute_hash(arg) for arg in args]


def hash_callable(func):
    """Hash the callable."""
    if not callable(func):
        raise ValueError("Function argument has to be callable")
    return _compute_hash(inspect.getsource(func))
