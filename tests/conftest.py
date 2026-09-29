import logging
import pytest


@pytest.fixture(autouse=True)
def set_logging_level():
    logging.basicConfig(level=logging.DEBUG)
