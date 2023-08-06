"""IO utils."""

import pickle
import typing as t


def load_cache(path: str) -> t.Any:
    """Load cached result for a given `key`."""
    with open(path, "rb") as file:
        obj = pickle.load(file)
    return obj


def dump_cache(path: str, obj: t.Any):
    """Dump object to cache."""
    with open(path, "wb") as file:
        pickle.dump(obj=obj, file=file)
