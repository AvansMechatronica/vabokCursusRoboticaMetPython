# Led Code Uitleg


## Wat doet deze code?
Deze code laat de ingebouwde LED op de Pico knipperen. Het is zoals een klein lampje dat steeds aan en uit gaat — precies 1 seconde aan, dan 1 seconde uit!

## Stap-voor-stap uitleg

```python
import machine
import time
```
**Wat gebeurt hier?**
We halen gereedschap uit onze "gereedschapskist":
- `machine`: geeft toegang tot de hardware van de Pico (zoals pinnen en LED's)
- `time`: voor het wachten tussen stappen

```python
led_onboard = machine.Pin(25, machine.Pin.OUT)
```
**Wat gebeurt hier?**
- `machine.Pin(25, ...)` kiest pin nummer 25 op de Pico — dit is de pin waarop de ingebouwde LED is aangesloten
- `machine.Pin.OUT` zegt: "deze pin is een *uitgang*", zodat de Pico stroom kan sturen naar de LED
- `led_onboard =` geeft deze pin een naam zodat we er makkelijk mee kunnen werken

```python
while True:
```
**Wat gebeurt hier?**
- `while True:` betekent: herhaal alles hieronder voor altijd (totdat de robot uit gaat)

```python
    led_onboard.value(1)
    time.sleep(1)
```
**Wat gebeurt hier?**
- `led_onboard.value(1)` zet de LED **aan** (1 = aan)
- `time.sleep(1)` wacht 1 seconde — de LED blijft 1 seconde branden

```python
    led_onboard.value(0)
    time.sleep(1)
```
**Wat gebeurt hier?**
- `led_onboard.value(0)` zet de LED **uit** (0 = uit)
- `time.sleep(1)` wacht weer 1 seconde — de LED blijft 1 seconde donker

## Hoe werkt een LED?
Een LED (Light Emitting Diode) is een klein lampje dat licht geeft zodra er stroom doorheen stroomt. Door de pin op 1 te zetten stuur je stroom naar de LED; bij 0 stopt de stroom en gaat de LED uit.

## Samengevat
De robot zet de ingebouwde LED steeds 1 seconde aan en 1 seconde uit — zo knipper je met de LED!
