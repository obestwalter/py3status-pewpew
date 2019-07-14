# -*- coding: utf-8 -*-
"""
PewPew + py3status = <3

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

@authors <your full name> <your email address>
@license BSD

SAMPLE OUTPUT
{'color': '#00FF00', 'full_text': '⎐'}
"""

import json
import threading
import time

import evdev
import serial  # pyserial

ACTION_EVENT = 1
AXIS_EVENT = 3

BUTTON_K_0 = 304
BUTTON_K_1 = 305

AXIS_VERTICAL = 1
AXIS_HORIZONTAL = 0

SERIAL_DEVICE = "/dev/ttyACM0"


class PewPewEvents(threading.Thread):

    state = None

    def __init__(self, parent):
        super(PewPewEvents, self).__init__()
        self.parent = parent

    def _set_state(self, state):
        self.state = state
        self.parent.py3.update()

    def get_pewpew_device(self):
        devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
        for device in devices:
            if "PewPew" in device.name:
                self.parent.py3.log("pewpew connected!")
                break
        else:
            raise Exception("pewpew not found")
        return evdev.InputDevice(device.path)

    def run(self):
        device = None
        while True:
            try:
                if device is None:
                    device = self.get_pewpew_device()
                    self._set_state(None)

                for event in device.read_loop():
                    if event.type == AXIS_EVENT:
                        if event.code == AXIS_HORIZONTAL:
                            if event.value == -127:
                                self._set_state("LEFT")
                            elif event.value == 127:
                                self._set_state("RIGHT")
                        elif event.code == AXIS_VERTICAL:
                            if event.value == -127:
                                self._set_state("UP")
                            elif event.value == 127:
                                self._set_state("DOWN")
                    elif event.type == ACTION_EVENT:
                        if event.code == BUTTON_K_0 and event.value == 1:
                            self._set_state("K0")
                        elif event.code == BUTTON_K_1 and event.value == 1:
                            self._set_state("K1")
            except Exception:
                if self.state is not False:
                    device = None
                    self._set_state(False)
                    self.parent.py3.log("pewpew disconnected!")
                time.sleep(1)


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
