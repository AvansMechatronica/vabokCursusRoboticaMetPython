# Import de pico_car bibliotheek
from pico_car import pico_car
from pico_car import ultrasonic
import time

# Maak een Motor object aan
Motor = pico_car()
ultrasonic = ultrasonic()

while True:
    # Lees afstand uit
    distance = ultrasonic.Distance_accurate()
    print("distance is %d cm"%(distance) )
    if distance > 10.0:
        Motor.Car_Run(255, 255)
    else:
        Motor.Car_Stop()
    time.sleep(1)
    
        

