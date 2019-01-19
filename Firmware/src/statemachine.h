#ifndef __STATEMACHINE_H
#define __STATEMACHINE_H

#include "hardware.h"
#include "SM.h"
#include "ktraining.h"

void ExecStatemachines();

void evalButtons(void (*f1)(), void (*f2)(), void (*f3)(), void (*f4)());
void smContinue();
void doNothing();
// STATES
State smStart();
State smSelectExerciseHead();
State smSelectExerciseBody();
State smCountdownHead();
State smCountdownBody();
State smDoingHead();
State smDoingBody();
State smPausedHead();
State smPausedBody();
State smFinishedHead();
State smFinishedBody();
State smCompleted();
// State smAdjustXXX();
// State smAbortXXX();
// State smDiscardXXX();
// State smReviewXXX();
// State smExitXXX();

// TRANSITIONS
void smSelectExercise();
void smStartCountdown();
void smStartExercise();
void smDoExercise();
void smPauseExercise();
void smFinishExercise();

#endif
