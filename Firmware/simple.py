import machine, neopixel
from utime import sleep

black  = (  0,   0,   0)
red    = (255,   0,   0)
green  = (  0, 255,   0)
blue   = (  0,   0, 255)
yellow = (255, 255,   0)

t_short = 0.05
t_long  = 0.33

np = neopixel.NeoPixel(machine.Pin(2), 1)

def set_np(color):
    np[0] = color
    np.write()

def blip(color, t_on, t_off):
    set_np(color)
    sleep(t_on)
    set_np(black)
    if t_off > 0:
        sleep(t_off)

def blip_1s(color, t_on):
    blip(color, t_on, 1.0 - t_on)

set_np(black)

# blip(red,   1, 0.1)
# blip(green, 1, 0.1)
# blip(blue,  1, 0.1)

sleep(2.0)

# countdown
for sec in range(0, 5):
    blip_1s (yellow, t_short)

for reps in range(0,10):
    # go up
    for sec in range(0,4):
        blip_1s (green, t_short)
    # stay up
    for sec in range(0,2):
        blip_1s (green, t_long)
    # go down
    for sec in range(0,4):
        blip_1s (red, t_short)
    # stay down
    for sec in range(0,2):
        blip_1s (red, t_long)

# finished!
blip(blue, 2, 0)
