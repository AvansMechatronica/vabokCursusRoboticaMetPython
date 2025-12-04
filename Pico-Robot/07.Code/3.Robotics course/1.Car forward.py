from pico_car import pico_car
import time

Motor = pico_car()

# Auto vooruit, parameter (Linker motor snelheid, Rechter motor snelheid), snelheid 0-255
Motor.Car_Run(255,255)
time.sleep(100)
# Auto stoppen
Motor.Car_Stop()