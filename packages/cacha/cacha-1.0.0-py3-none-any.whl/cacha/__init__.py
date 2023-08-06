"""
The cacha module provides the main functionality of the package.

The provided API helps managing the cache easily.
For example:

.. code:: python

    import cacha

    result = compute(data) # regular usage, slow
    result = cacha.cache(compute, (data, ))  # usage with cache

"""
import os

from cacha.version import __version__  # pylint: disable=unused-import

import cacha.store.pickledb_store
import cacha.store.store_interface
import cacha.manager
import cacha.logging_utils

cacha.logging_utils.configure_loggers(root_module_name=__name__)

cache = cacha.manager.cache


def configure_cache(
    cache_root: str, cache_dir_name: str, db_file_name: str
) -> cacha.store.store_interface.KeyValueStore:
    """Configure cache store.

    The files will be store under the provided path.

    Args:
        cache_root: path to cache root
        cache_dir_name: name of cache directory
        db_file_name: name of cache file
    """
    os.makedirs(os.path.join(cache_root, cache_dir_name), exist_ok=True)
    db_path = os.path.join(cache_root, cache_dir_name, db_file_name)
    store = cacha.store.pickledb_store.PickleDbStore(db_path=db_path)
    return store
