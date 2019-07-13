import pew
import supervisor

pew.init()
screen = pew.Pix()
prev_state = 0

screen.pixel(0, 0, 3)
pew.show(screen)

while True:
    if supervisor.runtime.serial_bytes_available:
        ux = input()
        if ux.isdigit():
            pix = pew.Pix.from_text(ux)
            screen.blit(pix, 0, 2)
            pew.show(screen)

    buttons = pew.keys()
    if buttons != prev_state:
        prev_state = buttons
    else:
        pew.tick(1 / 12)
        continue

    if buttons & pew.K_O:
        print(5)
    if buttons & pew.K_X:
        print(6)
    if buttons & pew.K_UP:
        print(pew.K_UP)
    if buttons & pew.K_DOWN:
        print(pew.K_DOWN)
    if buttons & pew.K_LEFT:
        print(pew.K_LEFT)
    if buttons & pew.K_RIGHT:
        print(pew.K_RIGHT)

    pew.show(screen)
    pew.tick(1 / 12)
