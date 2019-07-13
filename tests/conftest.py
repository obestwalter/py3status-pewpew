import pytest

from src.pew3wm.pew3wm import init_logging


@pytest.fixture(scope="session", autouse=True)
def setup_logging():
    init_logging()
