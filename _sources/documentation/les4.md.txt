# Les 4: Programmeren van actoren

Een actor is een apparaat dat signalen van een computer of microcontroller omzet in fysieke acties, zoals beweging of lichtsignalen af te geven. Op de pico-robot zijn verschillende actoren aanwezig die je kunt programmeren om je robot te laten bewegen en reageren op de omgeving.

## Motoren

De pico-robot heeft twee motoren die de wielen aandrijven. Je kunt deze motoren programmeren om vooruit, achteruit, links of rechts te bewegen. Hier is een voorbeeld van hoe je de motoren kunt aansturen:

```python
# Import de pico_car bibliotheek
from pico_car import pico_car
import time

# Maak een Motor object aan
Motor = pico_car()

print("Robot start met bewegen!")

# Auto vooruit, parameter (Linker motor snelheid, Rechter motor snelheid)
# Snelheid kan tussen 0-255 zijn
Motor.Car_Run(255, 255)

# Wacht 5 seconden
time.sleep(5)

# Stop de auto
Motor.Car_Stop()

print("Robot gestopt!")
```

De uitleg van dit Python-programma vind je in de [Motor Code Uitleg](les3_eerste_robot_programma.md).

:::{note}
De robot gaat rijden!!! Plaats de robot op een open oppervlak voordat je dit programma uitvoert, of houd de robot vast terwijl je het programma uitvoert.
:::

### Opdracht 1
Expirimenteer met verschillende snelheden en richtingen door de parameters van `Motor.Car_Run()` aan te passen. Probeer bijvoorbeeld de robot langzaam vooruit te laten rijden of een bocht naar links te maken.

## Opdracht 2
Maak een programma dat de robot dat de volgende stappen uitvoert:
* 3 seconden vooruit 
* bocht naar rechts (door de linker motor sneller te laten draaien dan de rechter) voor 2 seconden
* 3 seconden vooruit
* stop 2 seconden
* 5 seconden achteruit
* stop


## LED
Op de pico-robot is ook een lampje aanwezig. We noemen zo'n lampje een LED (Light Emitting Diode). Je kunt deze LED aan- en uitzetten met je programma. Hier is een voorbeeld:

```python
import machine 
import time 
led_onboard = machine.Pin(25, machine.Pin.OUT)

while True: 
    # Zet de LED aan
    led_onboard.value(1) 
    # Wacht 1 seconde
    time.sleep(1) 
    # Zet de LED uit
    led_onboard.value(0) 
    # Wacht 1 seconde
    time.sleep(1)
```

De uitleg van dit Python-programma vind je in de [LED Code Uitleg](les4_uitleg_led.md).

### Opdracht
Breid het programma van de motoren uit door de LED aan te zetten wanneer de robot vooruit rijdt en uit te zetten wanneer de robot stopt.

## Display
Op de pico-robot zit ook een klein schermpje, een OLED-display. OLED staat voor "Organic Light Emitting Diode". Je kent mischien de term wel van de OLDE-tv, deze werkt op dezefde principe. Je kunt hier tekst en eenvoudige afbeeldingen op weergeven. Hier is een voorbeeld van hoe je het OLED-display kunt gebruiken:

```python
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
```

De uitleg van dit Python-programma vind je in de [Display Code Uitleg](les4_uitleg_display.md).

### Opdracht
Programmeer een programma dat de tekst "Pico Robot" op het OLED-display toont wanneer de robot vooruit rijdt en "Stopped" wanneer de robot stopt. 

## Buzzer
De pico-robot heeft ook een buzzer, een klein apparaatje dat geluid kan maken. Je kunt deze buzzer gebruiken om geluidssignalen te geven. Hier is een voorbeeld van hoe je de buzzer kunt aansturen:

```python
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
```
De uitleg van dit Python-programma vind je in de [Buzzer Code Uitleg](les4_uitleg_buzzer.md).

### Opdracht
Programmeer een programma dat een piepje afspeelt op de buzzer wanneer de robot vooruit rijdt en stopt wanneer de robot stopt.

### Next Level: NeoPixels
De pico-robot heeft ook een rijtje van 8 kleine 3 kleuren-leds, ook wel NeoPixels genoemd. Deze kleuren leds zitten aan de onderkant van de robot. Deze kunnen in verschillende kleuren oplichten. Hier is een voorbeeld van hoe je de NeoPixels kunt aansturen:

```python
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
```
De uitleg van dit Python-programma vind je in de [NeoPixel Code Uitleg](les3_uitleg_neopixel.md).