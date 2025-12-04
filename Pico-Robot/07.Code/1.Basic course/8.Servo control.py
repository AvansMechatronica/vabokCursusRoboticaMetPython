from pico_car import pico_car

Servo = pico_car()

# 180 graden servo S1 hoek 0
# De parameters zijn (servo nummer, servo hoek)
Servo.servo180(1,0)
# 270 graden servo
Servo.servo270(2,90)
# 360 graden servo
Servo.servo360(3,360)