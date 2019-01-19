#include "hardware.h"

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);
Adafruit_NeoPixel led = Adafruit_NeoPixel(NUM_LEDS, PIN_LED, NEO_GRB + NEO_KHZ800);

void hwInit() {
  pinMode(PIN_BTN_1, INPUT_PULLUP);
  pinMode(PIN_BTN_2, INPUT_PULLUP);
  pinMode(PIN_BTN_3, INPUT_PULLUP);
  pinMode(PIN_BTN_4, INPUT_PULLUP);
  pinMode(PIN_BUZZER, OUTPUT);
  digitalWrite(PIN_BUZZER, LOW);

  Wire.begin(PIN_SDA, PIN_SCL);
  if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C, true, false)) { // Address 0x3D for 128x64
    Serial.println(F("SSD1306 error"));
    for(;;);
  }
  display.clearDisplay();
  display.fillRect(0, 0, 127, 63, WHITE);
  display.display();

  led.begin();
  led.setPixelColor(0, 0, 255, 32);
  led.show();

  delay(500);

  led.setPixelColor(0, 0, 0, 0);
  led.show();
  display.clearDisplay();
  display.display();
}
