from statemachine import StateMachine
from ktraining import kTraining, kExercise
import time

A1  = kExercise("A1",   240, {"Bew.": 15})
B6  = kExercise("B6",   170, {"Sitz": 19, "Lehne": 1, "Position": 6})
F1  = kExercise("F1",    40, {"Loch": 3})
F21 = kExercise("F2.1",  60, {"Loch": 4, "Fuss": 7})
F3  = kExercise("F3",   180, {"Fuss": 12, "Knie": 8, "Start": 3, "Bew.": 15})
C1  = kExercise("C1",   136, {"Sitz": 6, "Lehne": "vorne", "Arme": 1})
C7  = kExercise("C7",   180, {"Polster": 6, "Bew.": "2-17"})
D5  = kExercise("D5",   118, {"Lehne": 3, "Arme": 3})
D6  = kExercise("D6",   130, {"Sitz": 7, "Lehne": 3, "Griffe": "vertikal"})
G5  = kExercise("G5",    94, {"Sitz": 5, "Polster": 18, "Kopf": 4})

mytraining = kTraining((A1,B6,F1,F21,F3,C1,C7,D5,D6,G5))
speed_factor = 100000.0

def sm_training_start(training):
    print("Welcome to kTrain!")
    # training.next()
    # training.next()
    # training.next()
    return ("sm_training_before", training)

def sm_training_before(training):
    # if (training.current_exercise.name == "C1"):
    #     print("Skipping exercise",training.current_exercise.name)
    #     training.current_exercise.skip()
    #     newState = "sm_training_after"
    # else:
    #     print("About to start exercise",training.current_exercise.name,"with params:", training.current_exercise.params)
    #     newState = "sm_training_during"
    print("About to start exercise",training.current_exercise.name,"with params:", training.current_exercise.params)
    newState = "sm_training_during"
    return (newState, training)

def sm_training_during(training):
    print("Doing exercise",training.current_exercise.name)
    # training.do()
    return ("sm_go_up", training)

def sm_go_up(training):
    # print("^")
    time.sleep(4.0 / speed_factor)
    return ("sm_stay_up", training)

def sm_stay_up(training):
    # print("-")
    time.sleep(2.0 / speed_factor)
    return ("sm_go_down", training)

def sm_go_down(training):
    # print("v")
    time.sleep(4.0 / speed_factor)
    return ("sm_stay_down", training)

def sm_stay_down(training):
    # print("_")
    time.sleep(2.0 / speed_factor)
    training.current_exercise.reps += 1
    if (training.current_exercise.reps >= training.max_reps):
        training.current_exercise.done = True
        newState = "sm_training_after"
    else:
        newState = "sm_go_up"
    return (newState, training)

def sm_training_after(training):
    print("Finished exercise",training.current_exercise.name)
    if training.is_complete:
        newState = "sm_training_complete"
    else:
        training.next_pending()
        newState = "sm_training_before"
    return (newState, training)

def sm_training_complete(training):
    print("Training is complete.")
    return ("sm_training_exit", training)

def sm_training_exit(training):
    return (sm_training_exit, None)

def sm_init():
    m.add_state("sm_training_start",    sm_training_start   )
    m.add_state("sm_training_before",   sm_training_before  )
    m.add_state("sm_training_during",   sm_training_during  )
    m.add_state("sm_go_up",             sm_go_up            )
    m.add_state("sm_stay_up",           sm_stay_up          )
    m.add_state("sm_go_down",           sm_go_down          )
    m.add_state("sm_stay_down",         sm_stay_down        )
    m.add_state("sm_training_after",    sm_training_after   )
    m.add_state("sm_training_complete", sm_training_complete)
    m.add_state("sm_training_exit",     None, end_state=1   )
    m.set_start("sm_training_start")

m = StateMachine()
sm_init()

mytraining.print_plan()
m.run(mytraining)
mytraining.print_plan()
