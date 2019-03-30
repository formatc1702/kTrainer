#ifndef __GUI_H
#define __GUI_H

#include "ktraining.h"
#include "hardware.h"

void guiWelcome();
void guiSelectExercise();
void guiCountdown();
void guiDoingExercise();
void guiPaused();
void guiFinishedExercise();
void guiAdjustExercise();
void guiTrainingComplete();

void guiTitleBar();
void guiSoftButtons(char b1, char b2, char b3, char b4);

#endif
