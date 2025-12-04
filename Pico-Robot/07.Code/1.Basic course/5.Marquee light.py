import time
from pico_car import ws2812b

num_leds = 8  # Aantal NeoPixels
# Pin waar NeoPixels zijn aangesloten
pixels = ws2812b(num_leds, 0)
# Zet alle leds aan
pixels.fill(10,10,10)
pixels.show()
# Lopend licht effect
while True:
    for i in range(num_leds):
        for j in range(num_leds):
            #pixel_nummer, rood, groen, blauw
            pixels.set_pixel(j,abs(i+j)%10,abs(i-(j+3))%10,abs(i-(j+6))%10)
        pixels.show()
        time.sleep(0.05)