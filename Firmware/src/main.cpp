#include <Arduino.h>

#include "hardware.h"
#include "ktraining.h"

struct kTraining testTraining;

void setup() {
  Serial.begin(115200);
  hwInit();
  strcpy(testTraining.exercises[0].name, "F3.1");
}

void loop() {
  if(digitalRead(PIN_BTN_1) == LOW) {
    Serial.println(testTraining.exercises[0].name);
  }
  if(digitalRead(PIN_BTN_2) == LOW) {
    testTraining.exercises[0].reps--;
    Serial.println(testTraining.exercises[0].reps);
  }
  if(digitalRead(PIN_BTN_3) == LOW) {
    testTraining.exercises[0].reps++;
    Serial.println(testTraining.exercises[0].reps);
  }
  if(digitalRead(PIN_BTN_4) == LOW) {
    Serial.println(sizeof(testTraining));
  }
  delay(100);
}
