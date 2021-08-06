"""Module for configuration handling
"""


def get_config() -> dict:
    """(Very) simple configuration
    """

    test_config = {
        "db_path": "sqlite+aiosqlite:///:memory:",
        "data_path": "dataset.csv",
    }

    return test_config
