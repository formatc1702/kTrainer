#ifndef __HARDWARE_H
#define __HARDWARE_H

#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define PIN_BTN_1   5
#define PIN_BTN_2  13
#define PIN_BTN_3   0
#define PIN_BTN_4   4
#define PIN_LED     2
#define PIN_BUZZER 15
#define PIN_SCL    12
#define PIN_SDA    14

#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels
#define OLED_RESET    -1 // Reset pin # (or -1 if sharing Arduino reset pin)

void hwInit();

#endif
