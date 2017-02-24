from machine import Pin, Timer
import utime as time

import micropython
micropython.alloc_emergency_exception_buf(100)

class button_debounce:
    def __init__(self, pin_number, debounce_time=0.1):
        self.pin = Pin(pin_number, Pin.IN, Pin.PULL_UP)
        self.debounce_time = debounce_time
        self.clicked = False
        self.counter = 0
        self.ticks   = 0
        self.pin.irq (trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=lambda p: self.edge())

    def wasclicked(self):
        if self.clicked == True:
            ret = True
            self.clicked = False
        else:
            ret = False
        return ret

    def edge(self):
        now = time.ticks_ms()
        if self.pin.value() == 0: # pressed
            diff = now - self.ticks # time.ticks_diff(now, self.ticks_down)
            if diff > self.debounce_time * 1000.0: # success!
                self.ticks = now
                self.clicked = True
                self.counter += 1
        else: # released
            self.ticks = now # reset debounce
            self.clicked = False
        
button_1 = button_debounce(0)
button_2 = button_debounce(4)
button_3 = button_debounce(5)

where = 0
while True:
    if button_1.wasclicked():
        if where > 0:
            where -= 1
        print(where)
    if button_2.wasclicked():
        print(where)
    if button_3.wasclicked():
        if where < 10:
            where += 1
        print(where)
 