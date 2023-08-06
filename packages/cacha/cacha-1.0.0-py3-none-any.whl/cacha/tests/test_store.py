"""This is an example test."""

import os
import json
import pathlib
import tempfile
import pytest

import cacha
import cacha.store.pickledb_store


HOME = str(pathlib.Path.home())


@pytest.fixture
def example_store_data():
    """Return the example json store key-value store."""
    return {"test_data.csv": "test_data.csv"}


def test_configure_cache_cache_dir_creation():
    """Check if the cache directory is created."""
    cache_dir_name = ".cache"
    db_file_name = "store.json"
    cacha.configure_cache(
        cache_root=HOME,
        cache_dir_name=cache_dir_name,
        db_file_name=db_file_name,
    )

    assert os.path.exists(os.path.join(HOME, cache_dir_name, db_file_name))


@pytest.fixture(name="example_store_data")
def test_store():
    """Test the standard behavior of the store."""
    with tempfile.TemporaryDirectory() as tmpfile:
        store_path = os.path.join(tmpfile, "test_store.json")
        with open(store_path, encoding="utf-8") as file:
            file.write(json.dumps(example_store_data))
        store = cacha.store.pickledb_store.PickleDbStore(db_path=store_path)

        path = store.get("test_data")
        assert path == "test_data.csv"

        store.set("test_data2", "test_data2.csv")
        path = store.get("test_data2")
        assert path == "test_data2.csv"
