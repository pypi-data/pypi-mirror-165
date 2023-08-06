"""Implementation of `cacha.store.store_interface` and pickledb."""

import os
import json
import pickledb
import cacha.store.store_interface


class PickleDbStore(cacha.store.store_interface.KeyValueStore):
    """See base class."""

    def __init__(self, db_path: str) -> None:
        """Create the store object."""
        super().__init__()
        self.db_path = db_path
        self.init_store()

    def init_store(self):
        """Initialize the json store."""
        if not os.path.exists(self.db_path):
            with open(self.db_path, "w", encoding="utf-8") as file:
                file.write(json.dumps({}))

        # pylint: disable=invalid-name
        self.db = pickledb.load(
            self.db_path,
            False,
        )

    def set(self, key, value):
        """See base class."""
        self.db.set(key, value)
        self.db.dump()

    def get(self, key):
        """See base class."""
        return self.db.get(key)
