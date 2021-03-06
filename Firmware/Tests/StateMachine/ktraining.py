max_reps = 10

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
            print (ex.name, '\t', status, "<" if self.curex == i else " ", '\t', "{:>3}".format(ex.weight))

class kExercise:
    def __init__(self, name, weight, params):
        self.name   = name
        self.weight = weight
        self.params = params
        self.done   = False
        self.reps   = 0

    def do(self):
        print ("Doing exercise", self.name)
        self.done = True

    def skip(self):
        self.reps = 0
        self.done = True

    @property
    def skipped(self):
        return True if (self.reps == 0 and self.done == True) else False

    def reset(self):
        self.reps = 0
        self.done = False
