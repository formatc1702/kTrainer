from machine import Pin, I2C
import ssd1306
from gfx import GFX
from ktraining import kTraining, kExercise
from debounce import button_debounce
from statemachine import StateMachine
import utime as time

i2c = I2C(scl=Pin(14), sda=Pin(16), freq=100000)
oled = ssd1306.SSD1306_I2C(128, 32, i2c)
g = GFX(128, 32, oled.pixel)

training = kTraining()
training.load_training("myplan.txt")

btn_left   = button_debounce(0)
btn_center = button_debounce(4)
btn_right  = button_debounce(5)

countdown = 0 # global!

speed_factor  =   50
speed_factor2 =    2

def s_start():
    oled.fill(0)
    oled.text("kTrain!",0,0)
    oled.text("exit/start/view",0,24)
    oled.show()
    while True:
        if btn_left.transition() == 1:
            return("s_exit")
        if btn_center.transition() == 1:
            training.reset()
            return("s_before")
        if btn_right.transition() == 1:
            return("s_review")

def s_before():
    oled.fill(0)
    # print("About to start exercise {} with weight {} and params: {}".format(training.current_exercise.name, training.current_exercise.weight, training.current_exercise.params))
    oled.text("Exercise {}".format(training.current_exercise.name),0,0)
    # print("(SKIPPED)" if training.current_exercise.skipped else ("(DONE)" if training.current_exercise.done else "(PENDING)"))
    oled.text("(SKIPPED)" if training.current_exercise.skipped else ("(DONE)" if training.current_exercise.done else "(PENDING)"),0,8)
    oled.text("abort/start/->",0,24)
    oled.show()
    while True:
        if btn_left.transition() == 1:
            return("s_abort")
        if btn_center.transition() == 1:
            oled.fill(0)
            oled.text("Doing {}".format(training.current_exercise.name),0,0)
            oled.text("cancel/x/skip",0,24)
            oled.show()
            global countdown
            countdown = 5
            return("s_countdown")
        if btn_right.transition() == 1:
            training.next()
            return("s_before")

def s_countdown():
    global countdown
    now = time.ticks_ms()
    oled.fill(0)
    oled.text("{}".format(countdown),0,0)
    oled.text("abort/x/skip",0,24)
    oled.show()
    while True:
        if time.ticks_ms() - now > 1000 / speed_factor2:
            countdown -= 1
            if countdown > 0:
                return("s_countdown")
            else:
                # print("")
                return("s_go_up")
        if btn_left.transition() == 1:
            # print("")
            training.current_exercise.reset()
            return("s_before")
        if btn_right.transition() == 1:
            # print("")
            training.current_exercise.skip()
            if training.is_complete:
                return("s_completed")
            else:
                training.next_pending()
                return("s_before")

def s_paused():
    oled.fill(0)
    oled.text("Training paused",0,0)
    oled.text("disc/cont/x",0,24)
    oled.show()
    while True:
        if btn_left.transition() == 1:
            return("s_discard")
        if btn_center.transition() == 1:
            global countdown
            countdown = 5
            return("s_countdown")
        if btn_right.transition() == 1:
            pass

def s_go_up():
    now = time.ticks_ms()
    # print(training.current_exercise.reps, "^", end="")
    oled.fill(0)
    oled.text("^ {}".format(training.current_exercise.reps),0,0)
    oled.text("x/pause/x",0,24)
    oled.show()
    while True:
        if btn_center.transition() == 1:
            return("s_paused")
        if time.ticks_ms() - now > 4000 / speed_factor:
            return("s_stay_up")

def s_stay_up():
    now = time.ticks_ms()
    oled.fill(0)
    oled.text("- {}".format(training.current_exercise.reps),0,0)
    oled.text("x/pause/x",0,24)
    oled.show()
    while True:
        if btn_center.transition() == 1:
            return("s_paused")
        if time.ticks_ms() - now > 2000 / speed_factor:
            return("s_go_down")

def s_go_down():
    now = time.ticks_ms()
    oled.fill(0)
    oled.text("v {}".format(training.current_exercise.reps),0,0)
    oled.text("x/pause/x",0,24)
    oled.show()
    while True:
        if btn_center.transition() == 1:
            return("s_paused")
        if time.ticks_ms() - now > 4000 / speed_factor:
            return("s_stay_down")

def s_stay_down():
    now = time.ticks_ms()
    oled.fill(0)
    oled.text("_ {}".format(training.current_exercise.reps),0,0)
    oled.text("x/pause/x",0,24)
    oled.show()
    while True:
        if btn_center.transition() == 1:
            return("s_paused")
        if time.ticks_ms() - now > 2000 / speed_factor:
            training.current_exercise.reps += 1
            if (training.current_exercise.reps >= training.max_reps):
                training.current_exercise.finish()
                # print("")
                # print("Done...")
                return("s_after")
            else:
                # print("")
                return("s_go_up")

def s_after():
    oled.fill(0)
    oled.text("Finished {}".format(training.current_exercise.name),0,0)
    oled.text("disc/cont/adj",0,24)
    oled.show()
    while True:
        if btn_left.transition() == 1:
            return("s_discard")
        if btn_center.transition() == 1:
            if training.is_complete:
                return("s_completed")
            else:
                training.next_pending()
                return("s_before")
        if btn_right.transition() == 1:
            return("s_adjust")

def s_adjust():
    oled.fill(0)
    # print("Current weight for exercise {}: {}".format(training.current_exercise.name,training.current_exercise.weight))
    oled.text("{} Weight".format(training.current_exercise.name),0,0)
    oled.text("{}".format(training.current_exercise.weight),0,8)
    oled.text("- / save / +",0,24)
    oled.show()
    while True:
        if btn_left.transition() == 1:
            training.current_exercise.weight -= 2
            return("s_adjust")
        if btn_center.transition() == 1:
            # print("Set weight for exercise {}: {}".format(training.current_exercise.name,training.current_exercise.weight))
            return("s_after")
        if btn_right.transition() == 1:
            training.current_exercise.weight += 2
            return("s_adjust")

def s_abort():
    oled.fill(0)
    oled.text("Abort training?",0,0)
    oled.text("no / x / yes",0,24)
    oled.show()
    while True:
        if btn_left.transition() == 1:
            return("s_before")
        if btn_right.transition() == 1:
            while not training.is_complete:
                training.current_exercise.skip()
                training.next_pending()
            return("s_completed")

def s_discard():
    oled.fill(0)
    oled.text("Discard {}?".format(training.current_exercise.name),0,0)
    oled.text("cancel/rst/skip",0,24)
    oled.show()
    while True:
        if btn_left.transition() == 1:
            if training.current_exercise.ongoing:
                return("s_paused")
            else:
                return("s_after")
        if btn_center.transition() == 1:
            training.current_exercise.reset()
            return("s_before")
        if btn_right.transition() == 1:
            training.current_exercise.skip()
            if training.is_complete:
                return("s_completed")
            else:
                training.next_pending()
                return("s_before")


def s_completed():
    oled.fill(0)
    oled.text("Training done.",0,0)
    oled.text("discard/save/x",0,24)
    oled.show()
    while True:
        if btn_left.transition() == 1:
            print("Training was discarded")
            return("s_start")
        if btn_center.transition() == 1:
            print("Training was saved")
            #training.save_training("savedplan.txt")
            return("s_start")

def s_review():
    oled.fill(0)
    print("Here is a review of your training:")
    training.print_plan()
    oled.text("Printed review",0,0)
    oled.text("on serial out",0,8)
    oled.text("x / OK / x",0,24)
    oled.show()
    while True:
        if btn_center.transition() == 1:
            return("s_start")

def s_exit():
    return(s_exit, None)

m = StateMachine()
m.add_state("s_start",      s_start    )
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

m.run()
