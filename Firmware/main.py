from debounce import button_debounce
from statemachine import StateMachine
from ktraining import kTraining, kExercise
import ktraining
import utime as time

btn_left   = button_debounce(0)
btn_center = button_debounce(4)
btn_right  = button_debounce(5)

mytraining = ktraining.load_training("myplan.txt")
mytraining.exercises[0].weight = 888
ktraining.save_training("newplan.txt", mytraining)
speed_factor  = 100
speed_factor2 =  10

def sm_training_start(training):
    print("Welcome to kTrain!")
    print("cancel / start / x")
    while True:
        if btn_center.transition() == 1:
            return ("sm_training_before", training)
        if btn_left.transition() == 1:
            return ("sm_training_complete", training)

def sm_training_before(training):
    print("About to start exercise",training.current_exercise.name,"with weight", training.current_exercise.weight, "and params:", training.current_exercise.params, "(SKIPPED)" if training.current_exercise.skipped else ("(DONE)" if training.current_exercise.done else "(PENDING)"))
    print("<- / start / ->")
    while True:
        if btn_left.transition() == 1:
            training.previous()
            return ("sm_training_before", training)
        if btn_center.transition() == 1:
            return ("sm_training_countdown", training)
        if btn_right.transition() == 1:
            training.next()
            return ("sm_training_before", training)

def sm_training_countdown(training):
    print("Doing exercise",training.current_exercise.name)
    for i in reversed(range(1,6)):
        print(i, "... ", end="")
        time.sleep(1.0 / speed_factor2)
    print("")
    return ("sm_go_up", training)

def sm_training_paused(training):
    print("Training paused")
    print("discard / continue / x")
    while True:
        if btn_left.transition() == 1:
            return ("sm_training_discard",training)
        if btn_center.transition() == 1:
            return ("sm_training_countdown",training)
        if btn_right.transition() == 1:
            pass

def sm_go_up(training):
    print(training.current_exercise.reps, "^", end="")
    time.sleep(4.0 / speed_factor)
    if btn_center.transition() == 1:
        return ("sm_training_paused", training)
    return ("sm_stay_up", training)

def sm_stay_up(training):
    print("-", end="")
    time.sleep(2.0 / speed_factor)
    return ("sm_go_down", training)

def sm_go_down(training):
    print("v", end="")
    time.sleep(4.0 / speed_factor)
    return ("sm_stay_down", training)

def sm_stay_down(training):
    print("_", end="")
    time.sleep(2.0 / speed_factor)
    training.current_exercise.reps += 1
    if (training.current_exercise.reps >= training.max_reps):
        training.current_exercise.finish()
        print(" ")
        print("Done...")
        return ("sm_training_after", training)
    else:
        print("")
        return ("sm_go_up", training)

def sm_training_after(training):
    print("Finished exercise", training.current_exercise.name)
    print("discard / continue / adjust")
    while True:
        if btn_left.transition() == 1:
            return ("sm_training_discard", training)
        if btn_center.transition() == 1:
            if training.is_complete:
                newState = "sm_training_complete"
            else:
                training.next_pending()
                newState = "sm_training_before"
            return (newState, training)
        if btn_right.transition() == 1:
            return ("sm_training_adjust", training)

def sm_training_adjust(training):
    print("Current weight for exercise", training.current_exercise.name, ":", training.current_exercise.weight)
    print("- / save / +")
    while True:
        if btn_left.transition() == 1:
            training.current_exercise.weight -= 2
            return ("sm_training_adjust", training)
        if btn_center.transition() == 1:
            print("Set weight for  for exercise", training.current_exercise.name, ":", training.current_exercise.weight)
            return ("sm_training_after", training)
        if btn_right.transition() == 1:
            training.current_exercise.weight += 2
            return ("sm_training_adjust", training)

def sm_training_discard(training):
    print("Discard exercise ", training.current_exercise.name, "?")
    print("cancel / reset / skip")
    while True:
        if btn_left.transition() == 1:
            if training.current_exercise.ongoing:
                return ("sm_training_paused", training)
            else:
                return ("sm_training_after", training)
        if btn_center.transition() == 1:
            training.current_exercise.reset()
            return ("sm_training_before", training)
        if btn_right.transition() == 1:
            training.current_exercise.skip()
            training.next_pending()
            return ("sm_training_before", training)


def sm_training_complete(training):
    print("Training is complete.")
    print("discard / save / x")
    while True:
        if btn_left.transition() == 1:
            print("Training was discarded")
            return ("sm_training_exit", training)
        if btn_center.transition() == 1:
            print("Training was saved")
            ktraining.save_training("savedplan.txt", training)
            return ("sm_training_exit", training)

def sm_training_exit(training):
    return (sm_training_exit, None)

def sm_init():
    m.add_state("sm_training_start",     sm_training_start    )
    m.add_state("sm_training_before",    sm_training_before   )
    m.add_state("sm_training_countdown", sm_training_countdown)
    m.add_state("sm_training_paused",    sm_training_paused   )
    m.add_state("sm_go_up",              sm_go_up             )
    m.add_state("sm_stay_up",            sm_stay_up           )
    m.add_state("sm_go_down",            sm_go_down           )
    m.add_state("sm_stay_down",          sm_stay_down         )
    m.add_state("sm_training_after",     sm_training_after    )
    m.add_state("sm_training_adjust",    sm_training_adjust   )
    m.add_state("sm_training_discard",   sm_training_discard  )
    m.add_state("sm_training_complete",  sm_training_complete )
    m.add_state("sm_training_exit",      None, end_state=1    )
    m.set_start("sm_training_start")

m = StateMachine()
sm_init()

mytraining.print_plan()
m.run(mytraining)
mytraining.print_plan()
