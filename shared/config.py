import configparser
import os

_config = None


def get_config():
    """Load and cache the application config from config.ini.

    Searches for config.ini by walking up from the current working directory
    to the project root (identified by containing config.ini).

    Returns:
        configparser.ConfigParser: The parsed configuration.

    Raises:
        FileNotFoundError: If config.ini cannot be found.
    """
    global _config
    if _config is not None:
        return _config

    # Search upward from cwd to find config.ini
    search_dir = os.getcwd()
    for _ in range(10):  # limit search depth
        candidate = os.path.join(search_dir, "config.ini")
        if os.path.isfile(candidate):
            _config = configparser.ConfigParser()
            _config.read(candidate)
            return _config
        parent = os.path.dirname(search_dir)
        if parent == search_dir:
            break
        search_dir = parent

    raise FileNotFoundError("config.ini not found. Ensure it exists in the project root.")


def get_mongo_config():
    """Return the [MongoDB] section of the config."""
    return get_config()["MongoDB"]
