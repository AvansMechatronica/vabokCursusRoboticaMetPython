from pico_car import pico_car
import time

Motor = pico_car()

# Auto vooruit, parameter (Linker motor snelheid, Rechter motor snelheid), snelheid 0-255
Motor.Car_Run(255,255)
time.sleep(1)
# Auto achteruit
Motor.Car_Back(255,255)
time.sleep(1)
# Links
Motor.Car_Run(0,255)
time.sleep(1)
# Rechts
Motor.Car_Run(255,0)
time.sleep(1)
# Draai naar links
Motor.Car_Left(255,255)
time.sleep(1)
# Draai naar rechts
Motor.Car_Right(255,255)
time.sleep(1)
# Auto stoppen
Motor.Car_Stop()