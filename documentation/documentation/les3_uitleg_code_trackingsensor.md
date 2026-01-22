# Trackingsensor Code Uitleg (Onderwijsniveau 4)

## Wat doet deze code?
Deze code leest de vier trackingsensoren uit die op je Pico-robot zitten. Deze sensoren helpen de robot om lijnen op de grond te volgen, zoals een zwarte streep op een witte vloer.

## Stap-voor-stap uitleg

```python
from machine import Pin, I2C
from pico_car import SSD1306_I2C
import time
```
**Wat gebeurt hier?**
We halen gereedschap uit onze "gereedschapskist":
- `Pin`: dit helpt de robot contact te maken met sensoren
- `I2C`: communicatiemiddel voor verbinding met apparaten
- `SSD1306_I2C`: code voor het scherm van de robot
- `time`: voor het wachten tussen metingen

```python
# Definieer de lijnvolg sensoren, 1-4 van links naar rechts
# Zwart wordt herkend als 0 en wit als 1
# Tracing_1 Tracing_2 Tracing_3 Tracing_4
#    2         3        4          5     
Tracing_1 = machine.Pin(2, machine.Pin.IN)
Tracing_2 = machine.Pin(3, machine.Pin.IN)
Tracing_3 = machine.Pin(4, machine.Pin.IN)
Tracing_4 = machine.Pin(5, machine.Pin.IN)
```
**Wat gebeurt hier?**
- We zeggen tegen de robot waar de 4 trackingsensoren zitten
- `Pin(2)`, `Pin(3)`, `Pin(4)`, `Pin(5)` zijn de verbindingspunten op de robot
- `machine.Pin.IN` betekent: "Dit is een ingang waar sensoren informatie naar sturen"
- De sensoren zijn genummerd van 1 tot 4, van links naar rechts
- `Tracing_1` is de linkersensor, `Tracing_4` is de rechtersensor

**Wat meten de sensoren?**
- `0` (nul) = ZWART → de sensor ziet een donkere lijn
- `1` (één) = WIT → de sensor ziet lichte ondergrond

```python
while True:
    print("T1: %d T2: %d T3: %d T4: %d "%(Tracing_1.value(),Tracing_2.value(),Tracing_3.value(),Tracing_4.value()))
```
**Wat gebeurt hier?**
- `while True:` = herhaal dit totdat de robot uit gaat
- `Tracing_1.value()` = vraag sensor 1: "Wat zie jij?"
- `%d` betekent: "zet hier een getal in" (0 of 1)
- Voorbeeld uitvoer: `T1: 0 T2: 0 T3: 1 T4: 1` betekent:
  - Sensor 1 ziet ZWART (op de lijn)
  - Sensor 2 ziet ZWART (op de lijn)
  - Sensor 3 ziet WIT (niet op de lijn)
  - Sensor 4 ziet WIT (niet op de lijn)

```python
    time.sleep(0.1)
```
**Wat gebeurt hier?**
Wacht 0,1 seconde (een tiende van een seconde) voordat je opnieuw kijkt.

## Hoe kan de robot dit gebruiken?
Met deze 4 sensoren kan de robot bepalen waar de lijn is:
- Alle sensoren op WIT = de lijn is verloren gegaan, zoek opnieuw!
- Sensor 2 en 3 op ZWART = je rijdt recht over de lijn!
- Alleen linkersensoren op ZWART = je bent naar links verschoven, stuur naar rechts!
- Alleen rechtersensoren op ZWART = je bent naar rechts verschoven, stuur naar links!

## Samengevat
De robot kan met deze 4 sensoren voelen of hij op een zwarte lijn staat of niet. Door alle 4 tegelijk te controleren, weet de robot precies waar de lijn is en kan hij deze volgen!
