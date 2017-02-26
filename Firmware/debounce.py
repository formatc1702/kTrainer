from machine import Pin, Timer
import utime as time

class button_debounce:
    def __init__(self, pin_number, debounce_down=0.01, debounce_up=0.1):
        # debouncing parameters
        self.debounce_down = debounce_down
        self.debounce_up   = debounce_up
        # internal state
        self.debounced   = 0 # 1=pressed, 0=released
        self.lastchecked = 0 # ms
        self.lastdown    = 0 # ms
        self.lastup      = 0 # ms
        # hardware stuff
        self.pin = Pin(pin_number, Pin.IN, Pin.PULL_UP)
        self.pin.irq (trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=lambda p: self.edge())

    def edge(self):
        now = time.ticks_ms()
        if   self.pin.value() == 0 and self.debounced == 0: # pressed
            self.lastdown = now
        elif self.pin.value() == 1 and self.debounced == 1: # released
            self.lastup   = now

    def transition(self): # 1=pressed, -1=released, 0=no change
        # update debouncer
        now = time.ticks_ms()
        if self.pin.value() == 0: # debounce press
            if now - self.lastdown > self.debounce_down * 1000.0:
                self.debounced = 1
        else: # debounce release
            if now - self.lastup   > self.debounce_up   * 1000.0:
                self.debounced = 0
        # check if new transition has happened
        if self.lastchecked == self.debounced: # no new change
            return 0
        else:
            self.lastchecked = self.debounced # don't return this transition again
            return 1 if self.debounced == 1 else -1

    def pressed(self):
        return self.debounced == 1

    def released(self):
        return self.debounced == 0
