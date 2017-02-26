import ktraining

t = ktraining.kTraining()

t.load_training("myplan.txt")

t.print_plan()

t.current_exercise.weight = 9999

t.save_training("dumbplan.txt")
