import logging

from pew3wm.pewpew import PewPewEvents


log = logging.getLogger(__name__)


def test_sanity():
    assert PewPewEvents


def test_pewpew_behaviour():
    class FakeParent:
        def __init__(self):
            self.py3 = {}

    parent = FakeParent()
    PewPewEvents(parent)
