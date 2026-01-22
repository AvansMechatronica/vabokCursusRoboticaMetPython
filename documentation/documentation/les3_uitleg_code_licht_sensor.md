# Licht Sensor Code Uitleg

## Wat doet deze code?
Deze code leest de waardes van twee lichtsensoren uit die op je Pico-robot zitten. Deze sensoren helpen de robot om licht op te sporen.

## Stap-voor-stap uitleg

```python
from pico_car import ds, SSD1306_I2C
from machine import Pin, I2C, ADC
import time
```
**Wat gebeurt hier?**
We importeren (= meenemen) gereedschap dat we nodig hebben:
- `pico_car`: speciale code voor de Pico-robot
- `ADC`: dit is een apparaat dat analoge waarden kan lezen (zoals sensoren)
- `time`: voor het wachten tussen metingen

```python
# Light1 -> GP27
# Light2 -> GP26
light1 = machine.ADC(27)
light2 = machine.ADC(26)
```
**Wat gebeurt hier?**
- We zeggen: "sensor 1 zit op poort 27" en "sensor 2 zit op poort 26"
- `ADC(27)` en `ADC(26)` maken de sensoren klaar om informatie door te geven

```python
while True:
    # Dit gaat voor altijd herhalen
    LightS1 = light1.read_u16()
    LightS2 = light2.read_u16()
```
**Wat gebeurt hier?**
- `while True:` betekent: blijf dit doen tot je robot wordt uitgeschakeld
- `read_u16()` vraagt aan de sensor: "Hoeveel licht zie je?" (een getal van 0 tot 65535)
- Dit getal slaan we op in `LightS1` en `LightS2` (twee variabelen = twee dozen om getallen in op te slaan)

```python
    print("light1 is %d"%(LightS1) )
    print("light2 is %d"%(LightS2) )
```
**Wat gebeurt hier?**
We laten zien wat de sensoren hebben gemeten:
- `print()` schrijft het naar het scherm
- `%d` betekent "zet hier een getal in"
- `%(LightS1)` betekent "gebruik de waarde van sensor 1"

```python
    time.sleep(0.5)
```
**Wat gebeurt hier?**
Wacht 0,5 seconden (een halve seconde) voordat je weer meet. Dit zodat je niet te veel gegevens krijgt.

## Samengevat
De robot kijkt steeds naar hoeveel licht beide sensoren zien en geeft die getallen door. Dit kan de robot gebruiken om te weten waar het meeste licht is!
