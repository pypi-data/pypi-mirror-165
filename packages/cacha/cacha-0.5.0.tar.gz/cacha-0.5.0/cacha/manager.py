"""The main functionality of cache-manager."""

# import hashlib
import os
import logging
import typing as t
import pathlib

import cacha.cacha_io
import cacha.store
import cacha.hashing_tools as ht


LOGGER = logging.getLogger(__name__)

HOME = str(pathlib.Path.home())


def cache(
    func: t.Callable, args: t.Any = None, kwargs: t.Any = None, key: str = None
) -> t.Any:
    """Cache the results.

    Args:
        func: function to cache
        key: the key that is used to select the cache. If provided, all the
            other arguments are ignored. If the key doesn't exist in
            the store, the value is computed and stored, it's loaded otherwise.
    """
    if args is None:
        args = ()
    if kwargs is None:
        kwargs = {}

    store = cacha.configure_cache(
        cache_root=HOME, cache_dir_name=".cacha", db_file_name="store.json"
    )

    if key is None:
        all_hashed_args = []
        all_hashed_args += ht.hash_arguments(args)
        all_hashed_args += ht.hash_arguments(kwargs)
        hashed_callable = ht.hash_callable(func)
        store_key = hashed_callable + "_".join(all_hashed_args)

    else:
        LOGGER.info("Caching based key: %s, because key was provided", key)
        store_key = key

    # Check if a key exists in the store
    cache_path = store.get(store_key)
    if cache_path:
        LOGGER.info("Cache loaded from: %s", cache_path)
        result = cacha.cacha_io.load_cache(path=cache_path)
    else:
        result = func(*args, **kwargs)  # type: ignore
        cache_path = os.path.join(HOME, ".cacha", store_key)
        cacha.cacha_io.dump_cache(path=cache_path, obj=result)
        store.set(store_key, cache_path)
    return result


if __name__ == "__main__":
    # Example usage of cacha

    import time

    def wait(seconds: int = 2):
        """Return example string after `seconds`."""
        time.sleep(seconds)
        return "Example string object"

    start = time.time()
    cache(wait, (2,))
    print(f"Took {time.time() - start}")

    start = time.time()
    cache(wait, (2,))
    print(f"Took {time.time() - start}")
