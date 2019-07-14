import logging

from pew3wm.pewpew import PewPewEvents


log = logging.getLogger(__name__)


def test_sanity():
    assert True


def test_path_finder():
    path = PewPewEvents.get_pewpew_device()
    print(f"Path is {path}")
    assert ["test"] == "WHATEVER"
