import machine, neopixel
np = neopixel.NeoPixel(machine.Pin(2), 1)
np[0]=(0,0,0)
np.write() # turn off RGB LED


import network
ap = network.WLAN(network.AP_IF)
ap.active(False) # disable WebREPL
