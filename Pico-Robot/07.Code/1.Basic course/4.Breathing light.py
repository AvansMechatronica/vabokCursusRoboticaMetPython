import time
from pico_car import ws2812b

num_leds = 8  # Aantal NeoPixels
# Pin waar NeoPixels zijn aangesloten
pixels = ws2812b(num_leds, 0)
# Zet alle leds uit
pixels.fill(0,0,0)
pixels.show()
# Definieer variabelen
i = 0
brightness = 0
fadeAmount = 1
# Ademhaling effect
while True:
    for i in range(num_leds):
        pixels.set_pixel(i,0,brightness,brightness)
    pixels.show()
    brightness = brightness + fadeAmount
    if brightness <= 0 or brightness >= 200:
        fadeAmount = -fadeAmount
    time.sleep(0.005)
