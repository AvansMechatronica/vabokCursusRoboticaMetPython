from machine import Pin, I2C
from pico_car import pico_car, ws2812b, SSD1306_I2C
import time

Motor = pico_car()
num_leds = 8  # Aantal NeoPixels
# Pin waar NeoPixels zijn aangesloten
pixels = ws2812b(num_leds, 0)
# Zet alle leds uit
pixels.fill(0,0,0)
pixels.show()
# Initialiseer OLED
i2c=I2C(1, scl=Pin(15),sda=Pin(14), freq=100000)
oled = SSD1306_I2C(128, 32, i2c)
# Definieer de lijnvolg sensoren, 1-4 van links naar rechts
# Zwart wordt herkend als 0 en wit als 1
# Tracing_1 Tracing_2 Tracing_3 Tracing_4
#    2         3        4          5     
Tracing_1 = machine.Pin(2, machine.Pin.IN)
Tracing_2 = machine.Pin(3, machine.Pin.IN)
Tracing_3 = machine.Pin(4, machine.Pin.IN)
Tracing_4 = machine.Pin(5, machine.Pin.IN)

while True:
    
    # Vier lijnvolg sensoren status
    # 0 0 0 X
    if Tracing_1.value() == 0 and Tracing_2.value() == 0:
        for i in range(num_leds):
            pixels.set_pixel(i,255,0,0)
        oled.text('Cliff', 0, 0)
        Motor.Car_Back(150,150)
        time.sleep(0.5)
        Motor.Car_Right(150,150)
        time.sleep(0.5)
        #time.sleep(0.08)
        
    # Vier lijnvolg sensoren status
    # X 0 0 0
    elif Tracing_3.value() == 0 and Tracing_4.value() == 0:
        for i in range(num_leds):
            pixels.set_pixel(i,255,0,0)
        oled.text('Cliff', 0, 0)
        Motor.Car_Back(150,150)
        time.sleep(0.5)
        Motor.Car_Left(150,150)
        time.sleep(0.5)
        #time.sleep(0.08)
      
    else:
        Motor.Car_Run(100,100)
        for i in range(num_leds):
            pixels.set_pixel(i,255,255,255)
        oled.fill(0)
        
    pixels.show()
    oled.show()
# In andere gevallen behoudt de auto de vorige status
