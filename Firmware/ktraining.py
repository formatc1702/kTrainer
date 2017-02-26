max_reps = 12

class kTraining:
    def __init__(self, exercises):
        self.exercises = exercises
        self.curex     = 0
        self.max_reps  = max_reps

    @property
    def current_exercise(self):
        return self.exercises[self.curex]

    @property
    def is_complete(self):
        for ex in self.exercises:
            if ex.done == False:
                return False
        else:
            return True

    def next(self):
        self.curex += 1
        if self.curex >= len(self.exercises): # wrap around
            self.curex = 0

    def previous(self):
        self.curex -= 1
        if self.curex < 0: # wrap around
            self.curex = len(self.exercises) - 1

    def next_pending(self):
        if not self.is_complete:
            while self.current_exercise.done == True:
                self.next()

    def do(self):
        if not self.is_complete:
            if (self.current_exercise.done == True):
                print("Exerecise", self.current_exercise.name,"is already done.")
            else:
                self.current_exercise.do()
        # if self.is_complete:
        #     print("The training is complete")

    def do_and_continue(self):
        self.do()
        self.next()

    def reset(self):
        for ex in self.exercises:
            ex.resed()
        self.curex = 0

    def print_plan(self):
        print("Training plan:")
        for i, ex in enumerate(self.exercises):
            if   ex.skipped:
                status = " S"
            elif ex.done:
                status = "X "
            else:
                status = "- "
            print ("{:<4}".format(ex.name), '\t', status, "<" if self.curex == i else " ", '\t', "{:>3}".format(ex.weight))

class kExercise:
    def __init__(self, name, weight, params):
        self.name    = name
        self.weight  = weight
        self.params  = params
        self.ongoing = False
        self.done    = False
        self.skipped = False
        self.reps    = 0

    def start(self):
        self.ongoing = True

    def finish(self):
        self.ongoing = False
        self.skipped = False
        self.done    = True

    def skip(self):
        self.ongoing = False
        self.reps    = 0
        self.skipped = True
        self.done    = True

    def reset(self):
        self.ongoing = False
        self.reps    = 0
        self.skipped = False
        self.done    = False

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
            ex = ex + (kExercise(name, int(weight), params),)
    return kTraining(ex)

def save_training(filename, training):
    with open(filename, 'w') as f:
        for ex in training.exercises:
            f.write(ex.name)
            f.write("\t")
            f.write(str(ex.weight))
            f.write("\n")
