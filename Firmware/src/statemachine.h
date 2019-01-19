#ifndef __STATEMACHINE_H
#define __STATEMACHINE_H

#include "hardware.h"
#include "SM.h"
#include "ktraining.h"

void ExecStatemachines();

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

#endif
