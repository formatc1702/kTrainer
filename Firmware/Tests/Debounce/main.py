import micropython
micropython.alloc_emergency_exception_buf(100)
from machine import Pin, Timer
import machine
from time import sleep
import esp

btn_old = 0;
btn = 0

def irq_btn_1(p):
    global btn
    global btn_old
    global deb
    sleep(0.05)
    btn_new = p.value()
    if btn_new != btn_old:
        if btn_new == 1:
            btn = p
        else:
            btn = 0
        btn_old = btn

# SETUP ############################
pin_led = Pin(2)
pin_btn_1 = Pin(15)
pin_btn_2 = Pin(13)

pin_led.init(Pin.OUT)
pin_btn_1.init(Pin.IN)
#pin_btn_2.init(Pin.IN)

pin_btn_1.irq (trigger=Pin.IRQ_RISING, handler=irq_btn_1)
pin_btn_2.irq (trigger=Pin.IRQ_RISING, handler=irq_btn_1)
# pin_btn_1.irq (trigger=Pin.IRQ_FALLING, handler=irq_btn_up)


state = STATE_SEL_EX
cur_ex = 0
countdown = 10

# GO ##############################
pin_led.low()

def doaction():
    if state == STATE_SEL_EX: ############
        if   btn == pin_btn_1:
            cur_ex += 1
        elif btn == pin_btn_2:
            state = STATE_COUNTDOWN
            
    elif state == STATE_COUNTDOWN: ############
        if    btn == pin_btn_1:
            print("stop")
        elif btn == pin_btn_2:
            print("cancel")
            state = STATE_SEL_EX
    execstate()

def execstate():
    print("state: ", state)
    if    state == STATE_SEL_EX:
        print("select exercise ", cur_ex)
    elif state == STATE_COUNTDOWN:
        print("countdown is ",countdown)

execstate()
while True:
#    btn = pin_btn_1.value()
    if btn != 0:
        doaction()
        btn = 0
    else:
        pin_led.high()
    # sleep(0.001)

state = 0


