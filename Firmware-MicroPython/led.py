from machine import Pin
import neopixel

black  = (  0,   0,   0)
red    = (255,   0,   0)
green  = (  0, 255,   0)
blue   = (  0,   0, 255)
yellow = (255, 255,   0)
orange = (255,  85,   0)

class LED:
    def __init__(self, pin):
        self.np = neopixel.NeoPixel(pin, 1)
        self.starttime = 0
        self.period = 0
        self.duty = 0
        self.color = (0,0,0)
        self.set((0,0,0))

    def set(self, color):
        self.np[0] = color
        self.np.write()

    def blip(self, color, t_on, t_off):
        self.set(color)
        time.sleep(t_on)
        self.set(black)
        if t_off > 0:
            time.sleep(t_off)

    def blip_1s(self, color, t_on):
        self.blip(color, t_on, 1.0 - t_on)

    def blink_start(self, now, color, period=1000, duty=0.5):
        self.starttime = now
        self.period = period
        self.duty = duty
        self.color = color

    def blink_go(self, now):
        if (now - self.starttime) % self.period < self.period * self.duty:
            self.set(self.color)
        else:
            self.set((0,0,0))
