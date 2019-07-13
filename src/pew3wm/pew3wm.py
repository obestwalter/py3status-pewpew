import evdev
import logging

log = logging.getLogger(__name__)
DEVICE_NAME = "PewPew"


def main():
    init()
    pewPewPath = find_pew_pew_path()
    pewPew = evdev.InputDevice(pewPewPath)
    for event in pewPew.read_loop():
        log.debug(event)


def find_pew_pew_path():
    devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
    for device in devices:
        if DEVICE_NAME in device.name:
            log.debug(f"found {device.name} at {device.fn} ({device.phys})" )
            return device


def init():
    logging.basicConfig(level=logging.DEBUG)


if __name__ == '__main__':
    main()
