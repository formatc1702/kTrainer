#ifndef __KTRAINING_H
#define __KTRAINING_H

#include <Arduino.h>

#define NUM_EXERCISES 12
#define NUM_REPS      10

enum {XPENDING, ONGOING, DONE, SKIPPED};
enum {GO_UP, STAY_UP, GO_DOWN, STAY_DOWN};

struct kParam {
  char param[2];
  uint16_t value;
};

struct kExercise {
  char name[4];
  uint16_t weight;
  struct kParam params[4];
  uint8_t status;
  uint8_t reps;
};

struct kTraining {
  struct kExercise exercises[NUM_EXERCISES];
  uint8_t currentExercise;
  uint8_t currentPosition;
};

void resetTraining();
boolean trainingComplete();
uint8_t currentExercise();
void nextExercise();
void previousExercise();
void startExercise();
void finishExercise();
void skipExercise();
void resetExercise();

#endif
