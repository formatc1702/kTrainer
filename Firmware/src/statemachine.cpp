#include "statemachine.h"
#include "ktraining.h"

SM myStateMachine(smStart);

int countdown = 0;

void ExecStatemachines() {
  EXEC(myStateMachine);
};

void smContinue() {
  myStateMachine.Restart();
}

void doNothing() {}

// BUTTONS //////////////////////////////////////

void evalButtons(void (*f1)(), void (*f2)(), void (*f3)(), void (*f4)()) {
  if     (digitalRead(PIN_BTN_1) == LOW) { f1(); smContinue();}
  else if(digitalRead(PIN_BTN_2) == LOW) { f2(); smContinue();}
  else if(digitalRead(PIN_BTN_3) == LOW) { f3(); smContinue();}
  else if(digitalRead(PIN_BTN_4) == LOW) { f4(); smContinue();}
  delay(100);
}
// STATES ///////////////////////////////////////

State smStart() {
  Serial.print("Started.");
  resetTraining();
  smSelectExercise();
}

State smSelectExerciseHead() {
  Serial.print("Select ex ");
  Serial.println(currentExercise());
}
State smSelectExerciseBody() {
  evalButtons(previousExercise, doNothing, smStartCountdown, nextExercise);
}

State smCountdownHead() {
  Serial.print("Countdown: ");
  Serial.println(countdown);
}
State smCountdownBody() {
  evalButtons(doNothing, doNothing, doNothing, doNothing);
  if(myStateMachine.Timeout(1000)) {
    if (countdown > 1) {
      countdown--;
      smContinue();
    } else {
      smStartExercise();
    }
  }
}

State smDoingHead() {
  Serial.println("Doing exercise");
}
State smDoingBody() {
  evalButtons(smSelectExercise, doNothing, smPauseExercise, doNothing);
  if(myStateMachine.Timeout(1000)) {
    if (currentReps() < NUM_MAX_REPS) {
      doRep();
      Serial.print(currentReps());
      Serial.println(" reps done");
      smContinue();
    } else {
      smFinishExercise();
    }
  }
}

State smPausedHead() {
  Serial.print("Exercise paused");
}
State smPausedBody() {
  evalButtons(doNothing, doNothing, smStartCountdown, doNothing);
}

// TRANSITIONS //////////////////////////////////

void smSelectExercise() {
  myStateMachine.Set(smSelectExerciseHead, smSelectExerciseBody);
}

void smStartCountdown() {
  countdown = 5;
  myStateMachine.Set(smCountdownHead, smCountdownBody);
}

void smPauseExercise() {
  myStateMachine.Set(smPausedHead, smPausedBody);
}

void smStartExercise() {
  Serial.println("Started exercise");
  resetExercise();
  myStateMachine.Set(smDoingHead, smDoingBody);
}

void smFinishExercise() {
  Serial.println("Finished exercise");
  smSelectExercise();
}
