#include "statemachine.h"
#include "ktraining.h"

SM myStateMachine(smStart);

void ExecStatemachines() {
  EXEC(myStateMachine);
};

// STATES ///////////////////////////////////////

State smStart() {
  Serial.print("Started.");
  resetTraining();
  myStateMachine.Set(smSelectExerciseHead, smSelectExerciseBody);
}

State smSelectExerciseHead() {
  Serial.print("Ex ");
  Serial.println(currentExercise());
}
State smSelectExerciseBody() {
  if(digitalRead(PIN_BTN_1) == LOW) {
    myStateMachine.Set(smSelectExerciseHead, smSelectExerciseBody);
  }
  if(digitalRead(PIN_BTN_2) == LOW) {
    previousExercise();
    myStateMachine.Set(smSelectExerciseHead, smSelectExerciseBody);
  }
  if(digitalRead(PIN_BTN_3) == LOW) {
    nextExercise();
    myStateMachine.Set(smSelectExerciseHead, smSelectExerciseBody);
  }
  if(digitalRead(PIN_BTN_4) == LOW) {

  }
  delay(100);
}
