# pew3wm

experimenting with controlling i3wm with pewpew and creating a py3status module for it.

Starting from [this gist](https://gist.github.com/hbrylkowski/3ea9c65b672748b4f6a85074dd6ee311):

```python
import evdev

devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
for device in devices:
    print(device.fn, device.name, device.phys)

device = evdev.InputDevice("/dev/input/event23")
print(device)
for event in device.read_loop():
print(event)
```

This works when setting the pewpew to the gamepad mode (doing this directly on the pewpew).
