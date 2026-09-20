import os
import pytest


@pytest.fixture(autouse=True)
def clean_state():
    for db_file in ["arc_status.db", "chain_log.db"]:
        if os.path.exists(db_file):
            os.remove(db_file)
    yield
    for db_file in ["arc_status.db", "chain_log.db"]:
        if os.path.exists(db_file):
            os.remove(db_file)