# Ultrasoon Sensor Code Uitleg (Onderwijsniveau 4)

## Wat doet deze code?
Deze code leest de afstand van de ultrasone sensor op je Pico-robot. Zo weet de robot hoe ver een object voor hem staat, bijvoorbeeld een muur of obstakel.

## Stap-voor-stap uitleg

```python
import time
from pico_car import ultrasonic
```
**Wat gebeurt hier?**
We halen gereedschap uit onze "gereedschapskist":
- `time`: om te wachten tussen metingen
- `ultrasonic`: de module waarmee we de afstandssensor gebruiken

```python
# Initialiseer ultrasone sensor
ultrasonic = ultrasonic()
```
**Wat gebeurt hier?**
- We maken de ultrasoonsensor klaar voor gebruik
- Vanaf nu kunnen we met `ultrasonic` metingen uitvoeren

```python
while True:
    # Lees afstand uit
    distance = ultrasonic.Distance_accurate()
    print("distance is %d cm"%(distance) )
```
**Wat gebeurt hier?**
- `while True:` betekent: blijf dit oneindig herhalen
- `Distance_accurate()` meet de afstand in centimeters
- Die waarde bewaren we in `distance`
- Met `print(...)` tonen we de gemeten afstand in de seriele monitor
- Voorbeeld uitvoer: `distance is 24 cm`

```python
    time.sleep(1)
```
**Wat gebeurt hier?**
Wacht 1 seconde voordat je opnieuw meet. Zo blijft de output rustig en leesbaar.

## Hoe werkt een ultrasoonsensor?
De sensor werkt met echo:
- Hij stuurt een ultrasoon geluidssignaal uit
- Dat signaal botst tegen een object
- De echo komt terug bij de sensor
- Met de tijd van heen en terug berekent de robot de afstand

## Hoe kan de robot dit gebruiken?
Met deze metingen kan de robot slim reageren:
- Kleine afstand = object dichtbij, dus remmen of stoppen
- Grotere afstand = pad is vrij, dus doorrijden
- Wisselende afstand = object beweegt of robot komt dichterbij

## Samengevat
De robot meet steeds de afstand tot objecten voor zich. Daardoor kan hij obstakels op tijd herkennen en veiliger rijden zonder te botsen.
