from ktraining import kTraining, kExercise

def file_open(filename):
    with open(filename) as f:
        for line in f:
            if(line[0] == " "):
                print("exercise", line)
            else:
                print("param:", line.split())

file_open("myparams.txt")
