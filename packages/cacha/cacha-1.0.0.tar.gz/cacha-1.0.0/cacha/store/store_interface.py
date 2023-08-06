"""Simple local disk database management."""
import abc


class KeyValueStore(abc.ABC):
    """Interface for a key-value store."""

    def set(self, key: str, value: str):
        """Set the key value pair."""

    def get(self, key: str) -> str:
        """Get the value for the key."""
