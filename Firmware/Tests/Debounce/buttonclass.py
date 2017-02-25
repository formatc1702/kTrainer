from machine import Pin, Timer
import utime as time

import micropython
micropython.alloc_emergency_exception_buf(100)

class button_debounce:
    def __init__(self, pin_number, debounce_down=0.05, debounce_up=0.10):
        self.pin = Pin(pin_number, Pin.IN, Pin.PULL_UP)
        self.debounce_down = debounce_down
        self.debounce_up = debounce_up
        self.clicked = False
        self.official = 0
        self.lastchecked = 0
        self.lastdown = 0
        self.lastup = 0
        self.counter = 0
        self.ticks   = 0
        self.pin.irq (trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=lambda p: self.edge())

    def edge(self):
        now = time.ticks_ms()
        if self.pin.value() == 0: # pressed
            self.lastdown = now
        else: # released
            self.lastup = now

    def check(self):
        now = time.ticks_ms()
        if self.pin.value() == 0:
            if now - self.lastdown > self.debounce_down * 1000.0:
                self.official = 1
        else:
            if now - self.lastup   > self.debounce_up * 1000.0:
                self.official = 0
        return self.official

    def changed(self):
        self.check()
        if self.lastchecked == self.official:
            return False
        else:
            self.lastchecked = self.official
            return True

    def lasttransition(self):
        # if was pressed: 1
        # if was released: -1
        # if nothing: 0
        pass


button_1 = button_debounce(0)
button_2 = button_debounce(4)
button_3 = button_debounce(5)

where = 0
while True:
    if button_1.changed():
        if button_1.official == 1:
            if where > 0:
                where -= 1
            print(where)
    if button_2.changed():
        if button_2.official == 1:
            print(where)
    if button_3.changed():
        if button_3.official == 1:
            if where < 10:
                where += 1
            print(where)
