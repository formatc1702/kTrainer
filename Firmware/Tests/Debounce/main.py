from machine import Pin
from debounce import button_debounce

pin_btn = Pin(15)

button = button_debounce(pin_btn)
