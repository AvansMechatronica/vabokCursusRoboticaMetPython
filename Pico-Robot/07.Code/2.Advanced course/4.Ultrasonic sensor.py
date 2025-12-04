import time
from machine import Pin, I2C
from pico_car import SSD1306_I2C, ultrasonic
# Initialiseer ultrasone sensor
ultrasonic = ultrasonic()
# Initialiseer OLED
i2c=I2C(1, scl=Pin(15),sda=Pin(14), freq=100000)
oled = SSD1306_I2C(128, 32, i2c)

while True:
    # Lees afstand uit
    distance = ultrasonic.Distance_accurate()
    print("distance is %d cm"%(distance) )
    # Toon afstand op OLED
    oled.text('distance:', 0, 0)
    oled.text(str(distance), 75, 0)
    oled.show()
    oled.fill(0)
    time.sleep(1)
