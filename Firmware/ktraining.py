max_reps = 10

class kTraining:
    def __init__(self, exercises=[]):
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

    def reset(self):
        for ex in self.exercises:
            ex.reset()
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
            print ("{:<4}\t{} {}\t{:>3}".format(ex.name, status, "<" if self.curex == i else " ", ex.weight))

    def load_params(self, filename):
        ex = []
        with open(filename) as f:
            for line in f:
                if(line[0] != " "):
                    exname = line.rstrip()
                    ex.append(kExercise(exname, 0, {}),)
                else:
                    (key, val) = line.split()
                    ex[-1].params[key] = val
        return ex

    def load_training(self, filename):
        candidates = self.load_params("myparams.txt")
        with open(filename) as f:
            for line in f:
                (name, weight) = line.split()
                params = {}
                for candidate in candidates:
                    if candidate.name == name:
                        params = candidate.params
                self.exercises.append(kExercise(name, int(weight), params))

    def save_training(self, filename):
        with open(filename, 'w') as f:
            for ex in self.exercises:
                f.write("{}\t{}\n".format(ex.name, str(ex.weight)))

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
