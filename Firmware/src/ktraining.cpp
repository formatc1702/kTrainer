#include "ktraining.h"

struct kTraining myTraining;

void resetTraining() {
  for (size_t i = 0; i < NUM_EXERCISES; i++) {
    myTraining.exercises[i].status = XPENDING;
    myTraining.exercises[i].reps   = 0;
  }
  myTraining.currentExercise = 0;
}

boolean trainingComplete() {
  for (size_t i = 0; i < NUM_EXERCISES; i++) {
    if (myTraining.exercises[i].status != DONE &&
        myTraining.exercises[i].status != SKIPPED)
      return false;
  }
  return true;
}

uint8_t currentExercise() {
  return myTraining.currentExercise;
}

void nextExercise() {
  myTraining.currentExercise++;
  if (myTraining.currentExercise >= NUM_EXERCISES)
    myTraining.currentExercise -= NUM_EXERCISES;
}

void previousExercise() {
  if (myTraining.currentExercise == 0)
    myTraining.currentExercise += NUM_EXERCISES;
  myTraining.currentExercise--;
}

void startExercise() {
  myTraining.exercises[myTraining.currentExercise].status = ONGOING;
  myTraining.currentPosition = GO_UP;
}

void doRep() {
  myTraining.exercises[myTraining.currentExercise].reps++;
}

uint8_t currentReps() {
  return myTraining.exercises[myTraining.currentExercise].reps;
}

void finishExercise() {
  myTraining.exercises[myTraining.currentExercise].status = DONE;
}

void skipExercise() {
  myTraining.exercises[myTraining.currentExercise].status = SKIPPED;
  myTraining.exercises[myTraining.currentExercise].reps   = 0;
}

void resetExercise() {
  myTraining.exercises[myTraining.currentExercise].status = XPENDING;
  myTraining.exercises[myTraining.currentExercise].reps   = 0;
}
