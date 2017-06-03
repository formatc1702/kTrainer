from machine import Pin, I2C
import led
import ssd1306
import bitmapfont
from ktraining import kTraining, kExercise
from debounce import button_debounce
from statemachine import StateMachine
import bitmaps
import utime as time

btn_1 = button_debounce( 5) # spare IO because Pin(16) doesn't support pull
btn_2 = button_debounce(13)
btn_3 = button_debounce( 0)
btn_4 = button_debounce( 4)

l = led.LED(Pin(2))
t_short = 0.05
t_long  = 0.33

DISP_W = const(128)
DISP_H = const( 64)
i2c  = I2C(scl=Pin(12), sda=Pin(14), freq=100000)
oled = ssd1306.SSD1306_I2C  (DISP_W, DISP_H, i2c)
oled.write_cmd(0xa0 | 0x00) # flip X
oled.write_cmd(0xc0 | 0x00) # flip Y
bf   = bitmapfont.BitmapFont(DISP_W, DISP_H, oled.pixel, oled.framebuf.fill_rect)
bf.init()
bmp = bitmaps.MyGFX(oled.pixel)

training = kTraining()
training.load_training("myplan.txt")

countdown = 0 # global!

speed_factor  =    1
speed_factor2 =    1


def s_start():
    l.set(led.black)
    oled.fill(0)
    bf.text('kTrain',0,0,3,1)
    bmp.button_icons4(bitmaps.BLANK, bitmaps.X, bitmaps.PLAY, bitmaps.REPORT)
    oled.show()
    while True:
        if btn_2.transition() == 1:
            return("s_exit")
        if btn_3.transition() == 1:
            training.reset()
            return("s_select")
        if btn_4.transition() == 1:
            return("s_review")

def s_select():
    return("s_before")

def s_before():
    l.set(led.black)
    oled.fill(0)
    oled.framebuf.fill_rect(0,0,26,18,1)
    n = training.current_exercise.name
    if len(n) <= 2:
        bf.text(n,1,1,2,0)
    else:
        bf.text(n[0],   1, 1,2,0)
        bf.text(n[1],  14, 2,1,0)
        bf.text(n[2:4],14,10,1,0)

    bmp.draw_bitmap(bitmaps.WEIGHT,28,0)
    oled.text("{:>3}".format(training.current_exercise.weight), 40,0)

    if   training.current_exercise.skipped:
        bmp_status = bitmaps.SKIPPED
    elif training.current_exercise.done:
        bmp_status = bitmaps.DONE
    else:
        bmp_status = bitmaps.PENDING
    bmp.draw_bitmap(bmp_status, 44, 12)

    for i, k in enumerate(training.current_exercise.params.items()):
        oled.text("{} {:>2}".format(k[0][0],k[1][0:2]),74,8*i)

    bmp.button_icons4(bitmaps.LEFT, bitmaps.X, bitmaps.PLAY, bitmaps.RIGHT)
    oled.show()

    while True:
        if btn_1.transition() == 1:
            training.previous()
            return("s_select")
        if btn_2.transition() == 1:
            return("s_abort")
        if btn_3.transition() == 1:
            global countdown
            countdown = 5
            return("s_countdown")
        if btn_4.transition() == 1:
            training.next()
            return("s_select")

def s_countdown():
    global countdown
    now = time.ticks_ms()
    l.set(led.black)
    oled.fill(0)
    oled.text("{}".format(countdown),0,0)
    bmp.button_icons4(bitmaps.X, bitmaps.BLANK, bitmaps.BLANK, bitmaps.SKIP)
    oled.show()
    while True:
        if time.ticks_ms() - now > 1000 / speed_factor2:
            countdown -= 1
            if countdown > 0:
                return("s_countdown")
            else:
                return("s_go_up")
        if btn_1.transition() == 1:
            training.current_exercise.reset()
            return("s_select")
        if btn_4.transition() == 1:
            training.current_exercise.skip()
            if training.is_complete:
                return("s_completed")
            else:
                training.next_pending()
                return("s_select")

def s_paused():
    l.set(led.black)
    oled.fill(0)
    oled.text("Training paused",0,0)
    bmp.button_icons3(bitmaps.X, bitmaps.PLAY, bitmaps.BLANK)
    oled.show()
    while True:
        if btn_1.transition() == 1:
            return("s_discard")
        if btn_2.transition() == 1:
            global countdown
            countdown = 5
            return("s_countdown")
        if btn_3.transition() == 1:
            pass

def s_go_up():
    oled.fill(0)
    oled.text("^ {}".format(training.current_exercise.reps),0,0)
    bmp.button_icons3(bitmaps.BLANK, bitmaps.PAUSE, bitmaps.BLANK)
    oled.show()
    starttime = time.ticks_ms()
    l.blink_start(starttime, led.green, 1000, t_short)
    while True:
        now = time.ticks_ms()
        if btn_2.transition() == 1:
            return("s_paused")
        if now - starttime > 4000 / speed_factor:
            return("s_stay_up")
        l.blink_go(now)

def s_stay_up():
    oled.fill(0)
    oled.text("- {}".format(training.current_exercise.reps),0,0)
    bmp.button_icons3(bitmaps.BLANK, bitmaps.PAUSE, bitmaps.BLANK)
    oled.show()
    starttime = time.ticks_ms()
    l.blink_start(starttime, led.green, 1000, t_long)
    while True:
        now = time.ticks_ms()
        if btn_2.transition() == 1:
            return("s_paused")
        if now - starttime > 2000 / speed_factor:
            return("s_go_down")
        l.blink_go(now)

def s_go_down():
    oled.fill(0)
    oled.text("v {}".format(training.current_exercise.reps),0,0)
    bmp.button_icons3(bitmaps.BLANK, bitmaps.PAUSE, bitmaps.BLANK)
    oled.show()
    starttime = time.ticks_ms()
    l.blink_start(starttime, led.orange, 1000, t_short)
    while True:
        now = time.ticks_ms()
        if btn_2.transition() == 1:
            return("s_paused")
        if now - starttime > 4000 / speed_factor:
            return("s_stay_down")
        l.blink_go(now)

def s_stay_down():
    oled.fill(0)
    oled.text("_ {}".format(training.current_exercise.reps),0,0)
    bmp.button_icons3(bitmaps.BLANK, bitmaps.PAUSE, bitmaps.BLANK)
    oled.show()
    starttime = time.ticks_ms()
    l.blink_start(starttime, led.orange, 1000, t_long)
    while True:
        now = time.ticks_ms()
        if btn_2.transition() == 1:
            return("s_paused")
        if now - starttime > 2000 / speed_factor:
            training.current_exercise.reps += 1
            if (training.current_exercise.reps >= training.max_reps):
                training.current_exercise.finish()
                return("s_after")
            else:
                return("s_go_up")
        l.blink_go(now)

def s_after():
    l.set(led.black)
    oled.fill(0)
    oled.text("Finished {}".format(training.current_exercise.name),0,0)
    bmp.button_icons3(bitmaps.X, bitmaps.PLAY, bitmaps.ADJUST)
    oled.show()
    while True:
        if btn_1.transition() == 1:
            return("s_discard")
        if btn_2.transition() == 1:
            if training.is_complete:
                return("s_completed")
            else:
                training.next_pending()
                return("s_select")
        if btn_3.transition() == 1:
            return("s_adjust")

def s_adjust():
    oled.fill(0)
    oled.text("{} Weight".format(training.current_exercise.name),0,0)
    oled.text("{}".format(training.current_exercise.weight),0,8)
    bmp.button_icons3(bitmaps.MINUS, bitmaps.CHECK, bitmaps.PLUS)
    oled.show()
    while True:
        if btn_1.transition() == 1:
            training.current_exercise.weight -= 2
            return("s_adjust")
        if btn_2.transition() == 1:
            return("s_after")
        if btn_3.transition() == 1:
            training.current_exercise.weight += 2
            return("s_adjust")

def s_abort():
    oled.fill(0)
    oled.text("Abort training?",0,0)
    bmp.button_icons3(bitmaps.X, bitmaps.BLANK, bitmaps.CHECK)
    oled.show()
    while True:
        if btn_1.transition() == 1:
            return("s_select")
        if btn_3.transition() == 1:
            while not training.is_complete:
                training.current_exercise.skip()
                training.next_pending()
            return("s_completed")

def s_discard():
    oled.fill(0)
    oled.text("Discard {}?".format(training.current_exercise.name),0,0)
    bmp.button_icons3(bitmaps.X, bitmaps.RESTART, bitmaps.SKIP)
    oled.show()
    while True:
        if btn_1.transition() == 1:
            if training.current_exercise.ongoing:
                return("s_paused")
            else:
                return("s_after")
        if btn_2.transition() == 1:
            training.current_exercise.reset()
            return("s_select")
        if btn_3.transition() == 1:
            training.current_exercise.skip()
            if training.is_complete:
                return("s_completed")
            else:
                training.next_pending()
                return("s_select")


def s_completed():
    l.set(led.black)
    oled.fill(0)
    oled.text("Training done.",0,0)
    oled.text("discard/save/x",0,24)
    oled.show()
    while True:
        if btn_1.transition() == 1:
            print("Training was discarded")
            return("s_start")
        if btn_2.transition() == 1:
            print("Training was saved")
            #training.save_training("savedplan.txt")
            return("s_start")

def s_review():
    oled.fill(0)
    print("Here is a review of your training:")
    training.print_plan()
    oled.text("Printed review",0,0)
    oled.text("on serial out",0,8)
    bmp.button_icons3(bitmaps.BLANK, bitmaps.CHECK, bitmaps.BLANK)
    oled.show()
    while True:
        if btn_2.transition() == 1:
            return("s_start")

def s_exit():
    l.set(led.black)
    return(s_exit, None)

m = StateMachine()
m.add_state("s_start",      s_start    )
m.add_state("s_select",     s_select   )
m.add_state("s_before",     s_before   )
m.add_state("s_countdown",  s_countdown)
m.add_state("s_paused",     s_paused   )
m.add_state("s_go_up",      s_go_up    )
m.add_state("s_stay_up",    s_stay_up  )
m.add_state("s_go_down",    s_go_down  )
m.add_state("s_stay_down",  s_stay_down)
m.add_state("s_after",      s_after    )
m.add_state("s_adjust",     s_adjust   )
m.add_state("s_abort",      s_abort    )
m.add_state("s_discard",    s_discard  )
m.add_state("s_completed",  s_completed)
m.add_state("s_review",     s_review   )
m.add_state("s_exit", None, end_state=1)
m.set_start("s_start")

# import micropython
# micropython.mem_info(1)

m.run()
