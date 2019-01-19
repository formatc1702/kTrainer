#include <Arduino.h>

#include "hardware.h"
#include "ktraining.h"

void setup() {
  Serial.begin(115200);
  hwInit();
  resetTraining();
}

void loop() {
  if(digitalRead(PIN_BTN_1) == LOW) {
    Serial.println(currentExercise());
  }
  if(digitalRead(PIN_BTN_2) == LOW) {
    previousExercise();
    Serial.println(currentExercise());
  }
  if(digitalRead(PIN_BTN_3) == LOW) {
    nextExercise();
    Serial.println(currentExercise());
  }
  if(digitalRead(PIN_BTN_4) == LOW) {

  }
  delay(100);
}
