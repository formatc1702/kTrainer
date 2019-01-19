#include <Arduino.h>

#include "hardware.h"
#include "statemachine.h"

void setup() {
  Serial.begin(115200);
  hwInit();
}

void loop() {
  ExecStatemachines();
}
