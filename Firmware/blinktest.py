import led
import machine
import utime as time

l = led.LED(machine.Pin(2))
l.blink_start(time.ticks_ms(), led.blue)

while True:
    l.blink_go(time.ticks_ms())
    time.sleep(0.1)
