from debounce import button_debounce
from statemachine import StateMachine
from ktraining import kTraining, kExercise
import utime as time

btn_left   = button_debounce(0)
btn_center = button_debounce(4)
btn_right  = button_debounce(5)

countdown = 0 # global!

speed_factor  =   10
speed_factor2 =    1

training = kTraining()
training.load_training("myplan.txt")

def s_start():
    print("Welcome to kTrain!")
    print("exit / start / review")
    while True:
        if btn_left.transition() == 1:
            return("s_exit")
        if btn_center.transition() == 1:
            training.reset()
            return("s_before")
        if btn_right.transition() == 1:
            return("s_review")

def s_before():
    print("About to start exercise",training.current_exercise.name,"with weight", training.current_exercise.weight, "and params:", training.current_exercise.params, "(SKIPPED)" if training.current_exercise.skipped else ("(DONE)" if training.current_exercise.done else "(PENDING)"))
    print("<- / start / ->")
    while True:
        if btn_left.transition() == 1:
            training.previous()
            return("s_before")
        if btn_center.transition() == 1:
            print("Doing exercise",training.current_exercise.name)
            print("cancel / x / skip")
            global countdown
            countdown = 5
            return("s_countdown")
        if btn_right.transition() == 1:
            training.next()
            return("s_before")

def s_countdown():
    global countdown
    now = time.ticks_ms()
    print(countdown, "... ", end="")
    while True:
        if time.ticks_ms() - now > 1000 / speed_factor2:
            countdown -= 1
            if countdown > 0:
                return("s_countdown")
            else:
                print("")
                return("s_go_up")
        if btn_left.transition() == 1:
            print("")
            training.current_exercise.reset()
            return("s_before")
        if btn_right.transition() == 1:
            print("")
            training.current_exercise.skip()
            if training.is_complete:
                return("s_completed")
            else:
                training.next_pending()
                return("s_before")

def s_paused():
    print("Training paused")
    print("discard / continue / x")
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
    print(training.current_exercise.reps, "^", end="")
    while True:
        if btn_center.transition() == 1:
            return("s_paused")
        if time.ticks_ms() - now > 4000 / speed_factor:
            return("s_stay_up")

def s_stay_up():
    now = time.ticks_ms()
    print("-", end="")
    while True:
        if btn_center.transition() == 1:
            return("s_paused")
        if time.ticks_ms() - now > 2000 / speed_factor:
            return("s_go_down")

def s_go_down():
    now = time.ticks_ms()
    print("v", end="")
    while True:
        if btn_center.transition() == 1:
            return("s_paused")
        if time.ticks_ms() - now > 4000 / speed_factor:
            return("s_stay_down")

def s_stay_down():
    now = time.ticks_ms()
    print("_", end="")
    while True:
        if btn_center.transition() == 1:
            return("s_paused")
        if time.ticks_ms() - now > 2000 / speed_factor:
            training.current_exercise.reps += 1
            if (training.current_exercise.reps >= training.max_reps):
                training.current_exercise.finish()
                print("")
                print("Done...")
                return("s_after")
            else:
                print("")
                return("s_go_up")

def s_after():
    print("Finished exercise", training.current_exercise.name)
    print("discard / continue / adjust")
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
    print("Current weight for exercise", training.current_exercise.name, ":", training.current_exercise.weight)
    print("- / save / +")
    while True:
        if btn_left.transition() == 1:
            training.current_exercise.weight -= 2
            return("s_adjust")
        if btn_center.transition() == 1:
            print("Set weight for exercise", training.current_exercise.name, ":", training.current_exercise.weight)
            return("s_after")
        if btn_right.transition() == 1:
            training.current_exercise.weight += 2
            return("s_adjust")

def s_discard():
    print("Discard exercise ", training.current_exercise.name, "?")
    print("cancel / reset / skip")
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
    print("Training is complete.")
    print("discard / save / x")
    while True:
        if btn_left.transition() == 1:
            print("Training was discarded")
            return("s_start")
        if btn_center.transition() == 1:
            print("Training was saved")
            #training.save_training("savedplan.txt")
            return("s_start")

def s_review():
    print("Here is a review of your training:")
    training.print_plan()
    print("x / OK / x")
    while True:
        if btn_center.transition() == 1:
            return("s_start")

def s_exit():
    return(s_exit, None)

def sm_init():
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
    m.add_state("s_discard",    s_discard  )
    m.add_state("s_completed",  s_completed)
    m.add_state("s_review",     s_review   )
    m.add_state("s_exit", None, end_state=1)
    m.set_start("s_start")

m = StateMachine()
sm_init()

m.run()
