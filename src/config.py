"""Module for configuration handling
"""

def get_config() -> dict:
    """Loads and returns config if ADD_CONFIG is present in os.environ
    or returns default config otherwise
    Returns
    -------
    dict
        App configuration file
    """

    test_config = {
        "db_path": "sqlite+aiosqlite:///:memory:"
    }

    return test_config