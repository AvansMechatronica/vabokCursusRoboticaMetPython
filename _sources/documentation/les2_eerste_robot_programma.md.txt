# Eerste Robot Programma - Uitleg Onderwijsniveau 4

## Wat doet dit programma?
Dit is het allereerste programma voor je Pico-robot! Het programma laat de robot 5 seconden vooruit rijden en stopt hem daarna.

## Stap-voor-stap uitleg

```python
# Import de pico_car bibliotheek
from pico_car import pico_car
import time
```
**Wat gebeurt hier?**
- We halen de robotcode (`pico_car`) in ons programma
- We halen ook de timer (`time`) in ons programma
- Dit is als het pakken van je gereedschap voordat je gaat bouwen

```python
# Maak een Motor object aan
Motor = pico_car()
```
**Wat gebeurt hier?**
- We zeggen tegen Python: "Maak een robot-besturing klaar"
- `Motor =` slaat dit op in een doos met het label "Motor"
- Nu kunnen we `Motor` gebruiken om de robot te besturen!

```python
print("Robot start met bewegen!")
```
**Wat gebeurt hier?**
- We schrijven een bericht naar het scherm: "Robot start met bewegen!"
- Dit helpt ons zien dat het programma is gestart

```python
# Auto vooruit, parameter (Linker motor snelheid, Rechter motor snelheid)
# Snelheid kan tussen 0-255 zijn
Motor.Car_Run(255, 255)
```
**Wat gebeurt hier?**
- `Motor.Car_Run()` zegt: "Robot, rij vooruit!"
- `(255, 255)` betekent: beide motoren op VOLLE SNELHEID (maximum = 255)
- Eerste getal = linkermotor snelheid
- Tweede getal = rechtermotor snelheid
- Beide gelijk = het robotje rijdt recht vooruit!

**Snelheid voorbeelden:**
- `Motor.Car_Run(255, 255)` = beide motoren vol → heel snel vooruit
- `Motor.Car_Run(128, 128)` = beide motoren half → langzaam vooruit
- `Motor.Car_Run(255, 128)` = links vol, rechts half → draait naar rechts
- `Motor.Car_Run(128, 255)` = links half, rechts vol → draait naar links

```python
# Wacht 5 seconden
time.sleep(5)
```
**Wat gebeurt hier?**
- `time.sleep(5)` betekent: "Wacht 5 seconden"
- Gedurende deze 5 seconden rijdt de robot gewoon door!
- Na 5 seconden gaat het programma verder

```python
# Stop de auto
Motor.Car_Stop()
```
**Wat gebeurt hier?**
- `Motor.Car_Stop()` zegt: "Robot, stop met rijden!"
- De motoren worden uitgeschakeld
- De robot stopt

```python
print("Robot gestopt!")
```
**Wat gebeurt hier?**
- We schrijven een bericht naar het scherm: "Robot gestopt!"
- Klaar! Het programma is afgelopen

## Wat gebeurt er als je het runt?
1. Het scherm laat zien: "Robot start met bewegen!"
2. De robot rijdt 5 seconden lang rechtuit
3. De robot stopt
4. Het scherm laat zien: "Robot gestopt!"

## Samengevat
Dit programma maakt je robot 5 seconden lang vooruit rijden en stopt hem dan. Het is je eerste "robotstap"! Met dit basisprincipe kun je veel meer maken, zoals bochten, achteruit rijden, en veel meer!
