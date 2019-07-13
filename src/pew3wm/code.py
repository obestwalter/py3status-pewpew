import pew
import supervisor

pew.init()
screen = pew.Pix()
x = 0
y = 0
ux = None
while True:
    if supervisor.runtime.serial_bytes_available:
        ux = input()
        if ux.isdigit():
            pix = pew.Pix.from_text(ux)
            screen.blit(pix, 0, 2)
    pew.show(screen)
    pew.tick(1/12)

