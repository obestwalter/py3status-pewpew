import logging
from collections import namedtuple


from pew3wm.pewpew import (
    PewPewEvents,
    ACTION_EVENT,
    AXIS_EVENT,
    AXIS_HORIZONTAL,
    AXIS_VERTICAL,
    BUTTON_DOWN,
    BUTTON_K0,
    BUTTON_K1,
    MAJOR,
    MINOR,
)

event = namedtuple("event", ["type", "code", "value"])

log = logging.getLogger(__name__)


def test_sanity():
    assert PewPewEvents


def test_pewpew_behaviour():
    class FakeParent:
        def __init__(self):
            self.py3 = {}

    said = []

    def say(something):
        said.append(something)

    parent = FakeParent()
    dut = PewPewEvents(parent, say)  # dut; Device Under Test
    dut.get_pewpew_device = lambda: "test"

    fake_events = [
        event(AXIS_EVENT, AXIS_HORIZONTAL, MINOR),
        event(AXIS_EVENT, AXIS_HORIZONTAL, MAJOR),
        event(AXIS_EVENT, AXIS_VERTICAL, MINOR),
        event(AXIS_EVENT, AXIS_VERTICAL, MINOR - 20),
        event(AXIS_EVENT, AXIS_VERTICAL, MAJOR),
        event(ACTION_EVENT, BUTTON_K0, BUTTON_DOWN),
        event(1, 2, 3),
        event(ACTION_EVENT, BUTTON_K1, BUTTON_DOWN),
    ]
    dut._get_events = lambda: fake_events
    dut.device = None
    dut._try()

    expected = [
        "Setting device to None",
        "Initialized",
        "Setting device to test",
        "Setting state to None",
        "Setting state to LEFT",
        "Setting state to RIGHT",
        "Setting state to UP",
        "Ignoring event (3, 1, -147)",
        "Setting state to DOWN",
        "Setting state to K0",
        "Ignoring event (1, 2, 3)",
        "Setting state to K1",
    ]
    print(said)
    assert said == expected
