from machine import Pin, I2C
from pico_car import SSD1306_I2C
import time

# Stel I2C pinnen in
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=100000)
# Initialiseer OLED
oled = SSD1306_I2C(128, 32, i2c)
# Toon "Hello" op OLED op positie 0,0
oled.text("Hello", 0, 0)
oled.show()
oled.fill(0)
time.sleep(1)
# Toon "World" op OLED op positie 0,10
oled.text("World", 0, 10)
oled.show()
oled.fill(0)
time.sleep(1)
# Toon pixel op positie 100,30
oled.pixel(100, 30, 1)
oled.show()
oled.fill(0)
time.sleep(1)
