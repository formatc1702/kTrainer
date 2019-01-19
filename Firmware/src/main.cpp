#include <Arduino.h>

#include "hardware.h"

void setup() {
  Serial.begin(115200);
  hwInit();
}

void loop() {
  if(digitalRead(PIN_BTN_1) == LOW) {
    Serial.println('1');
  }
  if(digitalRead(PIN_BTN_2) == LOW) {
    Serial.println('2');
  }
  if(digitalRead(PIN_BTN_3) == LOW) {
    Serial.println('3');
  }
  if(digitalRead(PIN_BTN_4) == LOW) {
    Serial.println('4');
  }
  delay(100);
}
