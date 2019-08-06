# -*- coding: utf-8 -*-
"""
Control i3wm with the PewPew (https://pewpew.readthedocs.io).

This py3status module displays the current i3 workspace
on a PewPew device, and make use of the buttons for various
i3 purposes. The default for buttons left and right
is to switch workspace, but all buttons are configurable.

Configuration parameters:
    button_down: List of commands to execute when DOWN button is pressed
        (default [])
    button_k0: List of commands to execute when K0 button is pressed
        (default [])
    button_k1: List of commands to execute when K1 button is pressed
        (default [])
    button_left: List of commands to execute when LEFT button is pressed
        (default ["i3-msg workspace previous_on_output"])
    button_right: List of commands to execute when RIGHT button is pressed
        (default ["i3-msg workspace next_on_output"])
    button_up: List of commands to execute when UP button is pressed
        (default [])
    cache_timeout: how often to (re)detect the current workspace (default 10)
    format: Format for module output (default "{state}")
    format_idle: output when PewPew is idle or disconnected (default "⎐")

Format placeholders:
    {state} name of the latest pressed button

@authors <the EuroPython py3status pewpew> <xxx>
@license BSD

Examples:
```
# display the pewpew as an icon
# show scratchpad on K0 press
# toggle the dpms py3status module by simulating a left click on it on K1 press
pewpew {
    format = "⎐"
    button_k0 = "i3-msg scratchpad show"
    button_k1 = "py3-cmd click 1 dpms"
}

# increase or decrease the volume on UP/DOWN press by simulating clicks on the
# volume_status module (if you have it loaded)
pewpew {
    button_up = "py3-cmd click 4 volume_status"
    button_down = "py3-cmd click 5 volume_status"
}
```

SAMPLE OUTPUT
{'color': '#00FF00', 'full_text': '⎐'}
"""
import logging

import json
import threading
import time

import evdev
import serial  # pyserial

ACTION_EVENT = 1
AXIS_EVENT = 3
AXIS_HORIZONTAL = 0
AXIS_VERTICAL = 1
BUTTON_DOWN = 1
BUTTON_K0 = 304
BUTTON_K1 = 305
MAJOR = 127
MINOR = -127

log = logging.getLogger(__name__)

SERIAL_DEVICE = "/dev/ttyACM0"

event_map = {
    (AXIS_EVENT, AXIS_HORIZONTAL, MINOR): "LEFT",
    (AXIS_EVENT, AXIS_HORIZONTAL, MAJOR): "RIGHT",
    (AXIS_EVENT, AXIS_VERTICAL, MINOR): "UP",
    (AXIS_EVENT, AXIS_VERTICAL, MAJOR): "DOWN",
    (ACTION_EVENT, BUTTON_K0, BUTTON_DOWN): "K0",
    (ACTION_EVENT, BUTTON_K1, BUTTON_DOWN): "K1",
}


class PewPewEvents(threading.Thread):

    state = None

    def __init__(self, parent, say=None):
        super(PewPewEvents, self).__init__()
        if say is not None:
            self._say = say

        self._set_device(None)
        self.parent = parent
        self._say("Initialized")

    # The 'say' function is here for automatic
    # testing purposes; see test_pewpew.py
    def _say(self, msg):
        pass

    def _set_device(self, device):
        self._say(f"Setting device to {device}")
        self.device = device

    def _set_state(self, state):
        self._say(f"Setting state to {state}")
        self.state = state
        self.parent.py3.update()

    def get_pewpew_device(self):
        devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
        for device in devices:
            if "PewPew" in device.name and not 'event-mouse' in device.name:
                log.info("pewpew connected!")
                self._say("PewPew in device.name")
                break
        else:
            raise Exception("pewpew not found")
        return evdev.InputDevice(device.path)

    def _get_events(self):
        return list[self.device.read_loop()]

    def _try(self):
        try:
            if self.device is None:
                self._set_device(self.get_pewpew_device())
                self._set_state(None)

            for event in self._get_events():
                event_tuple = event.type, event.code, event.value
                new_state = event_map.get(event_tuple, None)
                if new_state is not None:
                    self._set_state(new_state)
                else:
                    self._say(f"Ignoring event {event_tuple}")

        except Exception:
            if self.state is not False:
                self._set_device(None)
                self._set_state(False)
                log.info("pewpew disconnected!")
            time.sleep(1)

    def run(self):
        while True:
            self._try()


class Py3status:

    # available configuration parameters
    button_down = []
    button_k0 = []
    button_k1 = []
    button_left = ["i3-msg workspace previous_on_output"]
    button_right = ["i3-msg workspace next_on_output"]
    button_up = []
    cache_timeout = 10
    format = "{state}"
    format_idle = "⎐"

    def post_config_hook(self):
        """
        This is the class constructor which will be executed once.
        """
        self._pewpew = PewPewEvents(self)
        self._pewpew.start()

    def _display_current_workspace(self):
        try:
            raw = self.py3.command_output("i3-msg -t get_workspaces")
            jsons = json.loads(raw)
            for j in jsons:
                if j["focused"]:
                    active = j["num"]
                    break
            else:
                active = 0
            # self.py3.log("active workspace is {}".format(active))
            with serial.Serial(SERIAL_DEVICE, 9600, timeout=1) as ser:
                ser.write(b"%d\r" % active)
        except Exception:
            pass

    def pewpew(self, *args, **kwargs):
        """
        """
        color = self.py3.COLOR_GOOD
        state = self._pewpew.state
        if state:
            button_exec = getattr(self, "button_{}".format(state.lower()), [])
            if isinstance(button_exec, str):
                button_exec = [button_exec]
            for cmd in button_exec:
                self.py3.command_run(cmd)
        elif state is False:
            state = self.format_idle
            color = self.py3.COLOR_BAD
        else:
            state = self.format_idle
        self._display_current_workspace()
        self._pewpew.state = None
        return {
            "cached_until": self.py3.time_in(self.cache_timeout),
            "color": color,
            "full_text": self.py3.safe_format(self.format, {"state": state}),
        }


if __name__ == "__main__":
    """
    Run module in test mode.
    """
    from py3status.module_test import module_test

    module_test(Py3status)
