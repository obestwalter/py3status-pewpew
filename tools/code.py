import struct
import time

import pew
import supervisor
import usb_hid

pew.init()
screen = pew.Pix()
prev_state = 0

for i in range(1, 5):
    screen.pixel(0, 0, i)
    time.sleep(1)
    pew.show(screen)
screen.pixel(0, 0, 0)
pew.show(screen)

for gamepad in usb_hid.devices:
    if gamepad.usage_page == 0x01 and gamepad.usage == 0x05:
        break
else:
    raise RuntimeError("Gamepad HID device not found")
report = bytearray(6)

while True:
    if supervisor.runtime.serial_bytes_available:
        ux = input()
        if ux.isdigit():
            # pew.init()
            # screen = pew.Pix()
            pix = pew.Pix.from_text(ux, color=3)
            if int(ux) < 10:
                screen.blit(pix, 2, 2)
            else:
                screen.blit(pix, 1, 2)

    buttons = pew.keys()
    report_buttons = 0

    if buttons & pew.K_O:
        report_buttons |= 0x01

    if buttons & pew.K_X:
        report_buttons |= 0x02

    if buttons & pew.K_UP:
        y = -127
    elif buttons & pew.K_DOWN:
        y = 127
    else:
        y = 0

    if buttons & pew.K_LEFT:
        x = -127
    elif buttons & pew.K_RIGHT:
        x = 127
    else:
        x = 0

    # print(report)
    struct.pack_into("<Hbbbb", report, 0, report_buttons, x, y, 0, 0)
    gamepad.send_report(report)
    pew.show(screen)
    pew.tick(1 / 12)
