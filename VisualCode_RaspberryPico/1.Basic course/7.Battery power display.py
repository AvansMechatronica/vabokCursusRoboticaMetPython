from machine import Pin, I2C, ADC
from pico_car import SSD1306_I2C
import time

# Initialiseer OLED
i2c=I2C(1, scl=Pin(15),sda=Pin(14), freq=100000)
oled = SSD1306_I2C(128, 32, i2c)
# Initialiseer ADC
Quantity_of_electricity = machine.ADC(28)

while True:
    # Toon batterijvermogen op OLED
    # Onder 20000 is de batterij leeg
    oled.text('Battery:', 0, 0)
    oled.text(str(Quantity_of_electricity.read_u16()), 65, 0)
    oled.show()
    oled.fill(0)
    time.sleep(0.1)
