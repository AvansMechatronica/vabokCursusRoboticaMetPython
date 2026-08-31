# Pico Car Bibliotheek - Functie Referentie

Dit document beschrijft alle functies en klassen in de `pico_car.py` bibliotheek voor de Raspberry Pi Pico Robot.

---

## Inhoudsopgave

1. [Klasse: pico_car](#klasse-pico_car)
2. [Klasse: ws2812b](#klasse-ws2812b)
3. [Klasse: ultrasonic](#klasse-ultrasonic)
4. [Klasse: SSD1306_I2C](#klasse-ssd1306_i2c)
5. [Klasse: ir](#klasse-ir)
6. [Klasse: ds](#klasse-ds)

---

## Klasse: pico_car

De hoofdklasse voor het besturen van de robot. Deze klasse regelt de motoren en servo's.

### Constructor

#### `__init__()`

Initialiseer de pico_car klasse.

**Gebruik:**
```python
Motor = pico_car()
```

**Wat doet het:**
- Stelt PWM frequenties in voor alle servo's (100 Hz)
- Stelt PWM frequenties in voor alle motoren (1000 Hz)
- Maakt de robot klaar voor gebruik

---

### Motor Functies

#### `Car_Run(speed1, speed2)`

Laat de robot vooruit rijden.

**Parameters:**
- `speed1` (int): Snelheid linker motor (0-255)
- `speed2` (int): Snelheid rechter motor (0-255)

**Voorbeeld:**
```python
Motor = pico_car()
Motor.Car_Run(255, 255)  # Volle snelheid vooruit
Motor.Car_Run(150, 150)  # Halve snelheid vooruit
Motor.Car_Run(200, 150)  # Vooruit met bocht naar rechts
```

**Uitleg:**
- 0 = motor staat stil
- 255 = maximale snelheid
- Verschillende snelheden voor linker en rechter motor zorgen voor bochten

---

#### `Car_Stop()`

Stop de robot volledig.

**Parameters:** Geen

**Voorbeeld:**
```python
Motor.Car_Stop()
```

**Uitleg:**
- Zet alle motor PWM signalen op 0
- Robot stopt met bewegen
- Gebruik dit altijd aan het einde van een beweging

---

#### `Car_Back(speed1, speed2)`

Laat de robot achteruit rijden.

**Parameters:**
- `speed1` (int): Snelheid linker motor (0-255)
- `speed2` (int): Snelheid rechter motor (0-255)

**Voorbeeld:**
```python
Motor.Car_Back(200, 200)  # Achteruit op volle snelheid
Motor.Car_Back(100, 150)  # Achteruit met bocht
```

**Uitleg:**
- Werkt hetzelfde als Car_Run maar dan in achterwaartse richting
- Verschillende snelheden zorgen voor bochten tijdens achteruitrijden

---

#### `Car_Left(speed1, speed2)`

Laat de robot op de plaats naar links draaien.

**Parameters:**
- `speed1` (int): Snelheid linker motor (0-255)
- `speed2` (int): Snelheid rechter motor (0-255)

**Voorbeeld:**
```python
Motor.Car_Left(150, 150)  # Draai links met gemiddelde snelheid
time.sleep(0.5)           # Draai een halve seconde
Motor.Car_Stop()
```

**Uitleg:**
- Linker motor draait achteruit
- Rechter motor draait vooruit
- Robot draait linksom op zijn as (spot turn)
- Hogere snelheid = snellere draaiing

---

#### `Car_Right(speed1, speed2)`

Laat de robot op de plaats naar rechts draaien.

**Parameters:**
- `speed1` (int): Snelheid linker motor (0-255)
- `speed2` (int): Snelheid rechter motor (0-255)

**Voorbeeld:**
```python
Motor.Car_Right(150, 150)  # Draai rechts met gemiddelde snelheid
time.sleep(0.5)            # Draai een halve seconde
Motor.Car_Stop()
```

**Uitleg:**
- Linker motor draait vooruit
- Rechter motor draait achteruit
- Robot draait rechtsom op zijn as
- De tijd bepaalt hoe ver de robot draait (bijv. 0.5s voor 90°)

---

### Servo Functies

#### `servo180(num, angle)`

Bestuur een 180 graden servo motor.

**Parameters:**
- `num` (int): Servo nummer (1, 2, 3 of 4)
- `angle` (int): Gewenste hoek (0-180 graden)

**Voorbeeld:**
```python
Motor.servo180(1, 90)   # Zet servo 1 naar middenpositie
Motor.servo180(2, 0)    # Zet servo 2 naar uiterst links
Motor.servo180(3, 180)  # Zet servo 3 naar uiterst rechts
```

**Uitleg:**
- Standaard servo met 180° bereik
- 0° = helemaal links
- 90° = midden
- 180° = helemaal rechts
- Veel gebruikt voor robotarmen, camera mounts, etc.

---

#### `servo270(num, angle)`

Bestuur een 270 graden servo motor.

**Parameters:**
- `num` (int): Servo nummer (1, 2, 3 of 4)
- `angle` (int): Gewenste hoek (0-270 graden)

**Voorbeeld:**
```python
Motor.servo270(1, 135)  # Zet servo 1 naar middenpositie
Motor.servo270(2, 0)    # Zet servo 2 naar uiterst links
Motor.servo270(2, 270)  # Zet servo 2 naar uiterst rechts
```

**Uitleg:**
- Servo met groter draaigebied (270° in plaats van 180°)
- Biedt meer bewegingsvrijheid
- 0° = uiterst links, 135° = midden, 270° = uiterst rechts

---

#### `servo360(num, speed)`

Bestuur een 360 graden (continue rotatie) servo motor.

**Parameters:**
- `num` (int): Servo nummer (1, 2, 3 of 4)
- `speed` (int): Rotatie snelheid/richting (0-360)

**Voorbeeld:**
```python
Motor.servo360(1, 180)  # Stop servo 1
Motor.servo360(2, 270)  # Draai servo 2 vooruit (halve snelheid)
Motor.servo360(3, 360)  # Draai servo 3 vooruit (volle snelheid)
Motor.servo360(4, 90)   # Draai servo 4 achteruit (halve snelheid)
Motor.servo360(4, 0)    # Draai servo 4 achteruit (volle snelheid)
```

**Uitleg:**
- Dit is geen standaard servo maar een continue rotatie motor
- Kan oneindig in beide richtingen draaien
- 0 = volle snelheid achteruit
- 180 = stop
- 360 = volle snelheid vooruit
- Handig voor wielen, transportbanden, etc.

---

## Klasse: ws2812b

Klasse voor het aansturen van WS2812B RGB LED strips (NeoPixels).

### Constructor

#### `__init__(num_leds, state_machine, delay=0.001)`

Initialiseer de LED strip.

**Parameters:**
- `num_leds` (int): Aantal LEDs in de strip
- `state_machine` (int): PIO state machine nummer (0-7)
- `delay` (float): Vertragingstijd na update in seconden (standaard 0.001)

**Voorbeeld:**
```python
pixels = ws2812b(8, 0)  # 8 LEDs, state machine 0
```

---

### LED Functies

#### `set_pixel(pixel_num, red, green, blue)`

Zet een individuele LED naar een specifieke kleur.

**Parameters:**
- `pixel_num` (int): LED nummer (0 tot num_leds-1)
- `red` (int): Rood component (0-255)
- `green` (int): Groen component (0-255)
- `blue` (int): Blauw component (0-255)

**Voorbeeld:**
```python
pixels.set_pixel(0, 255, 0, 0)    # LED 0 helder rood
pixels.set_pixel(1, 0, 255, 0)    # LED 1 helder groen
pixels.set_pixel(2, 0, 0, 255)    # LED 2 helder blauw
pixels.set_pixel(3, 255, 255, 0)  # LED 3 geel (rood + groen)
pixels.set_pixel(4, 255, 0, 255)  # LED 4 magenta (rood + blauw)
pixels.set_pixel(5, 0, 255, 255)  # LED 5 cyaan (groen + blauw)
pixels.set_pixel(6, 255, 255, 255) # LED 6 wit (alle kleuren)
pixels.show()  # VERGEET NIET OM show() AAN TE ROEPEN!
```

**Belangrijke kleuren:**
- `(255, 0, 0)` = Rood
- `(0, 255, 0)` = Groen
- `(0, 0, 255)` = Blauw
- `(255, 255, 0)` = Geel
- `(255, 0, 255)` = Magenta
- `(0, 255, 255)` = Cyaan
- `(255, 255, 255)` = Wit
- `(0, 0, 0)` = Uit

---

#### `set_pixel_line(pixel1, pixel2, red, green, blue)`

Zet een reeks LEDs naar dezelfde kleur.

**Parameters:**
- `pixel1` (int): Start LED nummer
- `pixel2` (int): Eind LED nummer (inclusief)
- `red, green, blue` (int): RGB kleurwaarden (0-255)

**Voorbeeld:**
```python
pixels.set_pixel_line(0, 3, 255, 0, 0)  # LEDs 0 t/m 3 rood
pixels.set_pixel_line(4, 7, 0, 0, 255)  # LEDs 4 t/m 7 blauw
pixels.show()
```

**Handig voor:**
- Snel meerdere LEDs tegelijk instellen
- Status indicatie met meerdere LEDs
- Zones maken op de LED strip

---

#### `set_pixel_line_gradient(pixel1, pixel2, left_red, left_green, left_blue, right_red, right_green, right_blue)`

Maak een vloeiend kleurverloop tussen twee LEDs.

**Parameters:**
- `pixel1` (int): Start LED
- `pixel2` (int): Eind LED
- `left_red, left_green, left_blue` (int): Start kleur RGB
- `right_red, right_green, right_blue` (int): Eind kleur RGB

**Voorbeeld:**
```python
# Gradient van rood naar blauw over alle 8 LEDs
pixels.set_pixel_line_gradient(0, 7, 255, 0, 0, 0, 0, 255)
pixels.show()

# Gradient van groen naar geel
pixels.set_pixel_line_gradient(0, 7, 0, 255, 0, 255, 255, 0)
pixels.show()
```

**Mooie effecten:**
- Regenboog effect
- Zonsondergang (rood → oranje → geel)
- Oceaan (blauw → groen → cyaan)

---

#### `fill(red, green, blue)`

Zet alle LEDs naar dezelfde kleur.

**Parameters:**
- `red, green, blue` (int): RGB kleurwaarden (0-255)

**Voorbeeld:**
```python
pixels.fill(255, 0, 0)  # Alle LEDs rood
pixels.show()

pixels.fill(0, 0, 0)    # Alle LEDs uit
pixels.show()

pixels.fill(255, 255, 255)  # Alle LEDs wit
pixels.show()
```

**Gebruik:**
- Snel alle LEDs dezelfde kleur geven
- LEDs uitzetten met (0, 0, 0)
- Status indicatie (rood = fout, groen = OK)

---

#### `brightness(brightness=None)`

Stel de helderheid in of lees deze uit.

**Parameters:**
- `brightness` (int, optioneel): Helderheid (1-255)
  - Als None: geeft huidige helderheid terug
  - Als getal: stelt nieuwe helderheid in

**Voorbeeld:**
```python
pixels.brightness(50)   # Zet helderheid op 50/255 (dimmen)
pixels.brightness(255)  # Maximale helderheid
pixels.brightness(1)    # Minimale helderheid (bijna uit)

current = pixels.brightness()  # Lees huidige helderheid
print("Helderheid:", current)
```

**Tip:**
- Gebruik lagere helderheid om stroom te besparen
- Bij heldere omgevingsverlichting: hogere helderheid
- Bij gebruik in het donker: lagere helderheid is prettiger

---

#### `rotate_left(num_of_pixels=1)`

Roteer alle LEDs een aantal posities naar links.

**Parameters:**
- `num_of_pixels` (int): Aantal posities (standaard 1)

**Voorbeeld:**
```python
# Maak een lopend licht effect
while True:
    pixels.rotate_left(1)
    pixels.show()
    time.sleep(0.1)
```

**Effect:**
- LED 0 → LED 7
- LED 1 → LED 0
- LED 2 → LED 1
- etc.

---

#### `rotate_right(num_of_pixels=1)`

Roteer alle LEDs een aantal posities naar rechts.

**Parameters:**
- `num_of_pixels` (int): Aantal posities (standaard 1)

**Voorbeeld:**
```python
# Maak een lopend licht effect (andere kant op)
while True:
    pixels.rotate_right(1)
    pixels.show()
    time.sleep(0.1)
```

---

#### `show()`

Stuur de LED data naar de strip en toon de kleuren.

**Parameters:** Geen

**Voorbeeld:**
```python
pixels.set_pixel(0, 255, 0, 0)  # Stel kleur in
pixels.set_pixel(1, 0, 255, 0)  # Stel kleur in
pixels.show()                    # NU pas worden kleuren zichtbaar!
```

**BELANGRIJK:**
- Je MOET show() aanroepen na het instellen van kleuren
- Zonder show() zie je geen veranderingen
- Je kunt meerdere set_pixel() aanroepen doen en dan één keer show()

---

## Klasse: ultrasonic

Klasse voor het uitlezen van de HC-SR04 ultrasone afstandssensor.

### Constructor

#### `__init__()`

Initialiseer de ultrasone sensor.

**Voorbeeld:**
```python
sensor = ultrasonic()
```

**Hardware:**
- Trigger pin: GPIO 0
- Echo pin: GPIO 1
- Bereik: 2cm tot 400cm
- Nauwkeurigheid: ±3mm

---

### Sensor Functies

#### `Distance()`

Voer een enkele afstandsmeting uit (basis functie).

**Parameters:** Geen

**Returns:** `float` - Afstand in centimeters

**Voorbeeld:**
```python
sensor = ultrasonic()
afstand = sensor.Distance()
print("Afstand:", afstand, "cm")
```

**Let op:**
- Deze functie kan soms onbetrouwbare metingen geven
- Gebruik bij voorkeur `Distance_accurate()` voor betere resultaten
- Geeft -1 terug bij een fout

---

#### `Distance_accurate()`

Voer een nauwkeurige afstandsmeting uit (aanbevolen).

**Parameters:** Geen

**Returns:** `int` - Gemiddelde afstand in centimeters

**Voorbeeld:**
```python
sensor = ultrasonic()
afstand = sensor.Distance_accurate()

if afstand < 20:
    print("Obstakel dichtbij!")
    Motor.Car_Stop()
elif afstand < 50:
    print("Voorzichtig rijden")
    Motor.Car_Run(100, 100)
else:
    print("Vrij baan")
    Motor.Car_Run(255, 255)
```

**Hoe werkt het:**
- Voert 5 metingen uit
- Filtert onbetrouwbare waarden
- Neemt gemiddelde van middelste 3 metingen
- Vermindert meetruis en geeft stabielere resultaten
- Geeft 999 terug bij een fout of buiten bereik

**Praktische toepassing:**
```python
# Obstakelvermijding
while True:
    afstand = sensor.Distance_accurate()
    
    if afstand < 15:
        # Te dichtbij! Draai weg
        Motor.Car_Back(150, 150)
        time.sleep(0.3)
        Motor.Car_Right(150, 150)
        time.sleep(0.5)
    else:
        # Rij vooruit
        Motor.Car_Run(200, 200)
    
    time.sleep(0.1)
```

---

## Klasse: SSD1306_I2C

Klasse voor het aansturen van een SSD1306 OLED display via I2C.

### Constructor

#### `__init__(width, height, i2c, addr=0x3c, external_vcc=False)`

Initialiseer het OLED display.

**Parameters:**
- `width` (int): Breedte in pixels (meestal 128)
- `height` (int): Hoogte in pixels (32 of 64)
- `i2c` (I2C): I2C bus object
- `addr` (int): I2C adres (standaard 0x3c)
- `external_vcc` (bool): Gebruik externe voeding (standaard False)

**Voorbeeld:**
```python
from machine import Pin, I2C
from pico_car import SSD1306_I2C

# Initialiseer I2C
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=100000)

# Initialiseer OLED (128x32 pixels)
oled = SSD1306_I2C(128, 32, i2c)
```

---

### Display Functies

#### `text(string, x, y, col=1)`

Toon tekst op het display.

**Parameters:**
- `string` (str): De tekst om te tonen
- `x` (int): X positie (0 = links)
- `y` (int): Y positie (0 = boven)
- `col` (int): Kleur (1 = wit, 0 = zwart)

**Voorbeeld:**
```python
oled.text("Hello", 0, 0)
oled.text("World", 0, 10)
oled.text("Robot!", 0, 20)
oled.show()  # Vergeet niet!
```

**Tips:**
- Lettergrootte is 8x8 pixels
- Maximum ~16 karakters per regel (bij 128 pixels breedte)
- Y-coördinaten: 0, 10, 20, 30 voor 4 regels tekst

---

#### `pixel(x, y, col)`

Zet een enkele pixel aan of uit.

**Parameters:**
- `x` (int): X positie (0-127)
- `y` (int): Y positie (0-31 of 0-63)
- `col` (int): 1 = aan, 0 = uit

**Voorbeeld:**
```python
# Teken een punt
oled.pixel(64, 16, 1)
oled.show()

# Teken een lijn van pixels
for i in range(128):
    oled.pixel(i, 16, 1)
oled.show()
```

---

#### `fill(col)`

Vul het hele scherm met een kleur.

**Parameters:**
- `col` (int): 0 = zwart (leeg scherm), 1 = wit (vol scherm)

**Voorbeeld:**
```python
# Maak scherm leeg
oled.fill(0)
oled.show()

# Vul scherm (test)
oled.fill(1)
oled.show()
```

**Gebruik:**
- `oled.fill(0)` voor het wissen van het scherm
- Doe dit voor je nieuwe tekst toont

---

#### `show()`

Toon de inhoud van de buffer op het display.

**Parameters:** Geen

**Voorbeeld:**
```python
oled.text("Test", 0, 0)
oled.show()  # NU pas verschijnt de tekst!
```

**BELANGRIJK:**
- Je MOET show() aanroepen om wijzigingen te zien
- Zonder show() verandert het scherm niet

---

### Praktische Voorbeelden OLED

#### Voorbeeld 1: Sensor waarde tonen
```python
from machine import Pin, I2C
from pico_car import SSD1306_I2C, ultrasonic
import time

# Initialiseer
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=100000)
oled = SSD1306_I2C(128, 32, i2c)
sensor = ultrasonic()

while True:
    afstand = sensor.Distance_accurate()
    
    # Wis scherm
    oled.fill(0)
    
    # Toon afstand
    oled.text('Afstand:', 0, 0)
    oled.text(str(afstand) + ' cm', 0, 10)
    oled.show()
    
    time.sleep(0.5)
```

#### Voorbeeld 2: Status display
```python
oled.fill(0)
oled.text('Robot Status', 0, 0)
oled.text('Batterij: 87%', 0, 10)
oled.text('Mode: Auto', 0, 20)
oled.show()
```

#### Voorbeeld 3: Scrollende tekst
```python
tekst = "Welkom bij de Pico Robot!"
x = 128  # Start rechts buiten beeld

while x > -len(tekst) * 8:  # 8 pixels per karakter
    oled.fill(0)
    oled.text(tekst, x, 12)
    oled.show()
    x -= 2  # Scroll snelheid
    time.sleep(0.05)
```

---

## Klasse: ir

Klasse voor het ontvangen van infrarood signalen van een afstandsbediening.

### Constructor

#### `__init__()`

Initialiseer de infrarood ontvanger.

**Voorbeeld:**
```python
from pico_car import ir

Ir = ir()
```

**Hardware:**
- IR ontvanger pin: GPIO 7
- Ondersteunt standaard NEC protocol afstandsbedieningen

---

### IR Functies

#### `Getir()`

Lees het ontvangen IR signaal.

**Parameters:** Geen

**Returns:** 
- `int`: Knop code (0-20)
- `None`: Geen knop ingedrukt

**Voorbeeld:**
```python
Ir = ir()

while True:
    knop = Ir.Getir()
    
    if knop != None:
        print("Knop ingedrukt:", knop)
        
        if knop == 1:  # Up knop
            Motor.Car_Run(255, 255)
        elif knop == 9:  # Down knop
            Motor.Car_Back(255, 255)
        elif knop == 4:  # Left knop
            Motor.Car_Left(150, 150)
        elif knop == 6:  # Right knop
            Motor.Car_Right(150, 150)
        elif knop == 5:  # OK knop
            Motor.Car_Stop()
    
    time.sleep(0.01)
```

**Knop codes:**
- 0 = Power
- 1 = Up
- 2 = Light
- 4 = Left
- 5 = OK/Sound
- 6 = Right
- 8 = Turn Left
- 9 = Down
- 10 = Turn Right
- 12 = Plus (+)
- 13 = Zero (0)
- 14 = Min (-)
- 16 = 1
- 17 = 2
- 18 = 3

---

### Praktisch Voorbeeld: Robot met afstandsbediening

```python
from pico_car import pico_car, ir
import time

Motor = pico_car()
Ir = ir()

print("Robot klaar! Gebruik afstandsbediening")

while True:
    knop = Ir.Getir()
    
    if knop != None:
        if knop == 1:  # Up
            print("Vooruit")
            Motor.Car_Run(200, 200)
            
        elif knop == 9:  # Down
            print("Achteruit")
            Motor.Car_Back(200, 200)
            
        elif knop == 4:  # Left
            print("Links")
            Motor.Car_Left(150, 150)
            
        elif knop == 6:  # Right
            print("Rechts")
            Motor.Car_Right(150, 150)
            
        elif knop == 5:  # OK/Sound (stop)
            print("Stop")
            Motor.Car_Stop()
            
        elif knop == 16:  # Knop 1 (langzaam)
            print("Langzaam vooruit")
            Motor.Car_Run(100, 100)
            
        elif knop == 17:  # Knop 2 (gemiddeld)
            print("Gemiddeld vooruit")
            Motor.Car_Run(150, 150)
            
        elif knop == 18:  # Knop 3 (snel)
            print("Snel vooruit")
            Motor.Car_Run(255, 255)
    
    time.sleep(0.01)
```

---

## Klasse: ds

Klasse voor het uitlezen van DS18B20 temperatuursensoren via OneWire protocol.

### Constructor

#### `__init__(unit='c', resolution=12)`

Initialiseer de temperatuursensor.

**Parameters:**
- `unit` (str): Temperatuur eenheid ('c' voor Celsius, 'f' voor Fahrenheit)
- `resolution` (int): Meetresolutie in bits (9, 10, 11 of 12)

**Voorbeeld:**
```python
from pico_car import ds

temp_sensor = ds(unit='c', resolution=12)
```

**Hardware:**
- OneWire data pin: GPIO 7
- Ondersteunt meerdere sensoren op één pin

---

### Temperatuur Functies

#### `read()`

Lees de temperatuur van alle aangesloten sensoren.

**Parameters:** Geen

**Returns:** `list` - Lijst met temperatuurwaarden (één per sensor)

**Voorbeeld:**
```python
temp_sensor = ds()
temperaturen = temp_sensor.read()

if temperaturen:
    for i, temp in enumerate(temperaturen):
        print(f"Sensor {i+1}: {temp}°C")
```

**Resolutie en meettijd:**
- 12 bit (standaard): 0.0625°C nauwkeurigheid, ~1000ms meettijd
- 11 bit: 0.125°C nauwkeurigheid, ~400ms meettijd
- 10 bit: 0.25°C nauwkeurigheid, ~200ms meettijd
- 9 bit: 0.5°C nauwkeurigheid, ~100ms meettijd

---

## Complete Voorbeelden

### Voorbeeld 1: Obstakelvermijding met LEDs en Display

```python
from pico_car import pico_car, ultrasonic, ws2812b, SSD1306_I2C
from machine import Pin, I2C
import time

# Initialiseer hardware
Motor = pico_car()
sensor = ultrasonic()
pixels = ws2812b(8, 0)
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=100000)
oled = SSD1306_I2C(128, 32, i2c)

print("Obstakelvermijding gestart!")

while True:
    afstand = sensor.Distance_accurate()
    
    # Update display
    oled.fill(0)
    oled.text('Afstand:', 0, 0)
    oled.text(str(afstand) + ' cm', 0, 10)
    
    if afstand < 15:
        # STOP! Te dichtbij
        Motor.Car_Stop()
        pixels.fill(255, 0, 0)  # Rood
        oled.text('STOP!', 0, 20)
        
    elif afstand < 30:
        # Langzaam rijden
        Motor.Car_Run(100, 100)
        pixels.fill(255, 255, 0)  # Geel
        oled.text('Voorzichtig', 0, 20)
        
    else:
        # Normale snelheid
        Motor.Car_Run(200, 200)
        pixels.fill(0, 255, 0)  # Groen
        oled.text('Vrije baan', 0, 20)
    
    pixels.show()
    oled.show()
    time.sleep(0.1)
```

### Voorbeeld 2: Lijnvolger met Feedback

```python
from pico_car import pico_car, ws2812b
from machine import Pin
import time

# Initialiseer
Motor = pico_car()
pixels = ws2812b(8, 0)

# Lijnvolg sensoren (GPIO 2-5)
sensor_L = Pin(2, Pin.IN)
sensor_ML = Pin(3, Pin.IN)
sensor_MR = Pin(4, Pin.IN)
sensor_R = Pin(5, Pin.IN)

# Snelheden
SNELHEID = 150
BOCHT_SNELHEID = 100

while True:
    # Lees sensoren (0 = zwart/lijn, 1 = wit/grond)
    links = sensor_L.value()
    midden_links = sensor_ML.value()
    midden_rechts = sensor_MR.value()
    rechts = sensor_R.value()
    
    # Logica voor lijnvolgen
    if midden_links == 0 and midden_rechts == 0:
        # Recht vooruit
        Motor.Car_Run(SNELHEID, SNELHEID)
        pixels.fill(0, 255, 0)  # Groen = goed
        
    elif midden_links == 0:
        # Draai iets naar links
        Motor.Car_Run(BOCHT_SNELHEID, SNELHEID)
        pixels.fill(0, 0, 255)  # Blauw = links
        
    elif midden_rechts == 0:
        # Draai iets naar rechts
        Motor.Car_Run(SNELHEID, BOCHT_SNELHEID)
        pixels.fill(255, 0, 255)  # Magenta = rechts
        
    elif links == 0:
        # Scherpe bocht links
        Motor.Car_Left(BOCHT_SNELHEID, BOCHT_SNELHEID)
        pixels.fill(0, 255, 255)  # Cyaan = scherp links
        
    elif rechts == 0:
        # Scherpe bocht rechts
        Motor.Car_Right(BOCHT_SNELHEID, BOCHT_SNELHEID)
        pixels.fill(255, 255, 0)  # Geel = scherp rechts
        
    else:
        # Lijn kwijt!
        Motor.Car_Stop()
        pixels.fill(255, 0, 0)  # Rood = fout
    
    pixels.show()
    time.sleep(0.01)
```

### Voorbeeld 3: Dashboard met alle sensoren

```python
from pico_car import ultrasonic, SSD1306_I2C, ds
from machine import Pin, I2C, ADC
import time

# Initialiseer hardware
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=100000)
oled = SSD1306_I2C(128, 32, i2c)
ultrasone = ultrasonic()
temp_sensor = ds()
batterij = ADC(28)

while True:
    # Lees alle sensoren
    afstand = ultrasone.Distance_accurate()
    temp = temp_sensor.read()
    bat_waarde = batterij.read_u16()
    bat_procent = int((bat_waarde / 65535) * 100)
    
    # Toon op display
    oled.fill(0)
    oled.text('Dashboard', 0, 0)
    oled.text(f'Afst:{afstand}cm', 0, 10)
    if temp:
        oled.text(f'Temp:{temp[0]:.1f}C', 0, 20)
    oled.text(f'Bat:{bat_procent}%', 70, 20)
    oled.show()
    
    time.sleep(0.5)
```

---

## Tips en Trucs

### Motorbesturing
1. **Start altijd met lagere snelheden** (100-150) om te testen
2. **Gebruik Car_Stop()** na elke beweging voor controle
3. **Experimenteer met tijd** - elke robot is anders
4. **Kalibreer je motoren** - pas snelheden aan als robot scheef rijdt

### LED Strip
1. **Vergeet show() niet** - zonder show() zie je niets!
2. **Gebruik lagere helderheid** om stroom te besparen
3. **Wis oude kleuren** met fill(0,0,0) voor schone effecten

### OLED Display
1. **fill(0) voor nieuwe tekst** om oude tekst te wissen
2. **Tekst past niet?** Gebruik kortere strings of kleinere font
3. **Update niet te snel** - 0.1s pauze is prima
4. **Test zonder robot** eerst om snelheid te controleren

### Ultrasone Sensor
1. **Gebruik Distance_accurate()** voor betrouwbare metingen
2. **Controleer op 999** (foutcode) in je code
3. **15cm minimum afstand** voor veilige stop
4. **Meet niet sneller dan 10x per seconde**

### Algemeen
1. **Test per onderdeel** - eerst motor, dan sensoren, dan combinatie
2. **Gebruik print()** om waarden te debuggen
3. **Voeg pauzes toe** met time.sleep() voor stabiele werking
4. **Documenteer je code** met comments voor later

---

## Troubleshooting

### Motor draait niet
- Controleer batterijen
- Controleer of PWM frequentie is ingesteld (gebeurt automatisch in __init__)
- Test met lagere snelheid (50-100)

### LEDs werken niet
- Heb je show() aangeroepen?
- Controleer GPIO 6 aansluiting
- Test met eenvoudige code eerst

### OLED toont niets
- Controleer I2C verbinding (GPIO 14 en 15)
- Heb je show() aangeroepen?
- Test met oled.fill(1) voor vol wit scherm

### Ultrasone sensor geeft 999
- Obstakel te dichtbij (< 2cm) of te ver (> 400cm)
- Controleer GPIO 0 en 1 verbindingen
- Test met Distance() eerst

### IR werkt niet
- Richt afstandsbediening recht op sensor
- Verwijder obstakels tussen zender en ontvanger
- Controleer batterijen in afstandsbediening
- Print knop waarde om te testen: `print(Ir.Getir())`

---

## Snelle Referentie Tabel

| Functie | Gebruik | Voorbeeld |
|---------|---------|-----------|
| `Car_Run(s1, s2)` | Rij vooruit | `Motor.Car_Run(255, 255)` |
| `Car_Stop()` | Stop robot | `Motor.Car_Stop()` |
| `Car_Back(s1, s2)` | Rij achteruit | `Motor.Car_Back(200, 200)` |
| `Car_Left(s1, s2)` | Draai links | `Motor.Car_Left(150, 150)` |
| `Car_Right(s1, s2)` | Draai rechts | `Motor.Car_Right(150, 150)` |
| `servo180(num, angle)` | Bestuur servo | `Motor.servo180(1, 90)` |
| `set_pixel(n, r, g, b)` | Zet LED kleur | `pixels.set_pixel(0, 255, 0, 0)` |
| `fill(r, g, b)` | Alle LEDs | `pixels.fill(0, 255, 0)` |
| `show()` | Toon LEDs | `pixels.show()` |
| `Distance_accurate()` | Meet afstand | `d = sensor.Distance_accurate()` |
| `text(str, x, y)` | Toon tekst | `oled.text("Hi", 0, 0)` |
| `Getir()` | Lees IR knop | `knop = Ir.Getir()` |

---

**Veel succes met programmeren van je Pico Robot!** 🤖
