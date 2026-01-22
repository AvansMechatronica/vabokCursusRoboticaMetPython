# Ultrasoon Sensor Code Uitleg

## Wat doet deze code?
Deze code meet de afstand tot objecten met een ultrasoon sensor. Dit is zoals "echolocatie" - net zoals vleermuizen geluid gebruiken om te zien waar dingen zijn!

## Stap-voor-stap uitleg

```python
import time
from machine import Pin, I2C
from pico_car import SSD1306_I2C, ultrasonic
```
**Wat gebeurt hier?**
We halen gereedschap uit onze "gereedschapskist":
- `time`: voor het wachten tussen metingen
- `Pin`, `I2C`: communicatiemiddelen voor verbinding met sensoren
- `ultrasonic`: speciale code voor de ultrasoon sensor

```python
# Initialiseer ultrasone sensor
ultrasonic = ultrasonic()
```
**Wat gebeurt hier?**
- We zeggen tegen de robot: "Zet de ultrasoon sensor klaar om te gebruiken"
- `ultrasonic()` maakt de sensor gereed voor actie

```python
while True:
    # Dit gaat voor altijd herhalen
    distance = ultrasonic.Distance_accurate()
```
**Wat gebeurt hier?**
- `while True:` betekent: herhaal dit totdat de robot uit gaat
- `Distance_accurate()` vraagt aan de sensor: "Hoe ver weg is het dichtsbijzijnde ding?"
- `distance =` slaat het antwoord op in een doos met het label "distance"

```python
    print("distance is %d cm"%(distance) )
```
**Wat gebeurt hier?**
- `print()` schrijft iets naar het scherm
- `%d` betekent "voeg hier een getal in"
- `"distance is %d cm"` schrijft bijvoorbeeld: "distance is 25 cm"
- `%(distance)` voegt het gemeten getal in

```python
    time.sleep(1)
```
**Wat gebeurt hier?**
Wacht 1 seconde (tellen: "een" en klaar!) voordat je de afstand opnieuw meet.

## Hoe werkt ultrasoon?
De sensor stuurt geluidsgolven uit (te hoog om te horen) en wacht tot ze terugkaatsen. Hoe sneller het geluid terugkomt, hoe dichterbij het object is!

## Samengevat
De robot meet continu hoe ver weg het dichtsbijzijnde object is (zoals een muur of persoon) en geeft dit getal af in centimeters. Dit kan de robot gebruiken om niet tegen dingen aan te rijden!
