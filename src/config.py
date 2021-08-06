"""Module for configuration handling
"""
from typing import Any, Dict

def get_config() -> Dict[str, Any]:
    """(Very) simple configuration
    """

    test_config = {
        "db_path": "sqlite+aiosqlite:///:memory:",
        "data_path": "dataset.csv",
    }

    return test_config
