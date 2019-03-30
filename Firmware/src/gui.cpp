#include "gui.h"

void guiWelcome() {
  // TODO: show ktrainer splash screen
}

void guiSelectExercise() {
  guiTitleBar();
  // TODO: show exercise number
  // TODO: show exercise params
  guiSoftButtons('{',' ','>','}');
}

void guiCountdown() {
  guiTitleBar();
  // TODO: show large countdown
  guiSoftButtons(' ','x',' ','s');
}

void guiDoingExercise() {
  guiTitleBar();
  // TODO: show exercise number
  // TODO: show exercise state (up/hold/down/hold)
  // TODO: show progress bar (of this rep)
  // TODO: show progress bar (of this exercise)
  guiSoftButtons(' ','p',' ','s');
}

void guiPaused() {
  guiTitleBar();
  // TODO: show exercise number
  // TODO: show reps left
  guiSoftButtons(' ','r','>','s');
}

void guiFinishedExercise() {
  guiTitleBar();
  // TODO: show exercise number
  // TODO: show current weight
  guiSoftButtons(' ','e','^',' ');
}

void guiAdjustExercise() {
  guiTitleBar();
  // TODO: show exercise number
  // TODO: show current weight
  guiSoftButtons('-','x','^','+');
}

void guiTrainingComplete() {
  // TODO: show congrats
  // TODO: show option to save to log
}

////////

void guiTitleBar() {

}

// { left arrow
// } right arrow
// > play
// p pause
// r return/repeat
// s skip
// e edit/adjust
// + plus
// - minus
// ^ yes/good/OK
// x no/bad

void guiSoftButtons(char b1, char b2, char b3, char b4) {

}
