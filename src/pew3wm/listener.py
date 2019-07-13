import evdev

ACTION_EVENT = 1
BUTTON_K_0 = 304
BUTTON_K_1 = 305
AXIS_VERTICAL = 1

AXIS_HORIZONTAL = 0

AXIS_EVENT = 3

devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
for device in devices:
    if "PewPew" in device.name:
        break
    print(device.fn, device.name, device.phys)
else:
    raise Exception("No valid input")

device = evdev.InputDevice(device.path)


def set_state(state):
    print(state)


for event in device.read_loop():
    if event.type == AXIS_EVENT:
        if event.code == AXIS_HORIZONTAL:
            if event.value == -127:
                set_state("LEFT")
            elif event.value == 127:
                set_state("RIGHT")
        elif event.code == AXIS_VERTICAL:
            if event.value == -127:
                set_state("UP")
            elif event.value == 127:
                set_state("DOWN")
    elif event.type == ACTION_EVENT:
        if event.code == BUTTON_K_0 and event.value == 1:
            set_state("K0")
        elif event.code == BUTTON_K_1 and event.value == 1:
            set_state("K1")

