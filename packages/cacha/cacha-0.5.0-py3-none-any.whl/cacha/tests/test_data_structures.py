"""This is an example test."""

import pandas as pd
import numpy as np
import cacha


def test_pandas():
    """Test caching for pandas object."""
    data = pd.DataFrame([[1, "a"], [2, "a"], [3, "b"]], columns=["A", "B"])

    cacha.cache(pd.get_dummies, (data,))

    cached = cacha.cache(pd.get_dummies, (data,))

    assert cached.shape[0] == 3
    assert cached.shape[1] == 3


def test_numpy():
    """Test caching for numpy object."""
    data = np.array([[1, 3], [3, 7]])

    cacha.cache(np.mean, kwargs={"a": data, "axis": 1})

    cached = cacha.cache(np.mean, kwargs={"a": data, "axis": 1})

    assert cached[0] == 2
    assert cached[1] == 5


def test_raw_text():
    """Test caching for string object."""
    string = "This is a long string"

    def split(string: str) -> list:
        return string.split()

    cacha.cache(split, (string,))

    cached = cacha.cache(split, (string,))

    assert len(cached) == 5
