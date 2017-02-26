from ktraining import kTraining, kExercise


def load_params(filename):
    ex = ()
    with open(filename) as f:
        for line in f:
            if(line[0] != " "):
                exname = line.rstrip()
                ex = ex + (kExercise(exname, 0, {}),)
                # print("exercise", exname)
            else:
                (key, val) = line.split()
                # print("param:", key, "value:", val)
                ex[-1].params[key] = val
    return ex

def load_training(filename):
    candidates = load_params("myparams.txt")
    ex = ()
    with open(filename) as f:
        for line in f:
            (name, weight) = line.split()
            params = {}
            for candidate in candidates:
                if candidate.name == name:
                    params = candidate.params
            ex = ex + (kExercise(name, weight, params),)
    return kTraining(ex)

def save_training(filename, training):
    with open(filename, 'w') as f:
        for ex in training.exercises:
            f.write(ex.name)
            f.write("\t")
            f.write(str(ex.weight))
            f.write("\n")

mytraining = load_training("myplan.txt")
mytraining.print_plan()
mytraining.exercises[1].weight = 999

save_training("newplan.txt", mytraining)
# newtraining = load_training("newplan.txt")
# newtraining.print_plan()
#
# print(mytraining.current_exercise.name)
# print(mytraining.current_exercise.params)
