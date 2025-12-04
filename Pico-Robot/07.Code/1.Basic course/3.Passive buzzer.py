from machine import Pin, PWM
import time
# Stel buzzer pin in
BZ = PWM(Pin(22))
BZ.freq(1000)
# Initialiseer muziek
CM = [0, 330, 350, 393, 441, 495, 556, 624] 
song = [CM[1],CM[1],CM[5],CM[5],CM[6],CM[6],CM[5],CM[4],CM[4],CM[3],CM[3],CM[2],CM[2],CM[1],]
beat = [ 0.5,0.5,0.5,0.5,0.5,0.5,1,0.5,0.5,0.5,0.5,0.5,0.5,1,]
# Muziek functie   
def music():
        print('Speelt liedje ...')
        for i in range(len(song)):
            BZ.duty_u16(500)
            BZ.freq(song[i])
            time.sleep(beat[i]) 
            BZ.duty_u16(0)
            time.sleep(0.01) 
# Speel muziek   
music()
print("Einde")


